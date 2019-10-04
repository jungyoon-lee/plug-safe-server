import json
from socket import *
from threading import Thread, Lock
from queue import Queue

from app.models.device import temp_master, Master, Slave
from app import db

# from app.routes.device import bytes_to_dict

host = '0.0.0.0'
port = 8081
address = (host, port)

sockNode_list_mutex = Lock()
socketNode_list = []

class socketNode:
    def __init__(self, c_sock, c_addr): # 전송할 데이터 추가
        self.client_sock = c_sock
        self.client_addr = c_addr
        self.mutex = Lock()
        self.newData = 0
        self.changes = 0
        self.RXAddr = []
        self.states = []

    def updateSlaveInfo(self, changes, RXAddr_list, states_list):
        #self.mutex.acquire()
        self.changes = changes
        self.RXAddr = RXAddr_list
        self.states = states_list
        self.newData = 1
        #self.mutex.release()


    def sendData(self):
        sign = False
        #self.mutex.acquire()
        if self.newData:
            data = {'changes': self.changes, 'slaves_addr': self.RXAddr, 'states': self.states}

            data_json = json.dumps(data).encode('utf-8')
            self.client_sock.sendall(data_json)

            # sendToMaster(self.client_sock, data)

            self.newData = False
            sign = True
        #self.mutex.release()

        return sign # 전송 됬는지 안됬는지


def runSocketServer():
    print('소켓 서버 실행')

    try:
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(address)
        server_socket.listen(10)

        print('서버 열림')
        print('포트 번호 %d 사용 중' % port)

        db_check_thread = Thread(target=checkChangeMaster, args=())
        db_check_thread.start()

        while True:
            client_socket, addr = server_socket.accept()
            print(str(addr), '에서 접속되었습니다.')

            # master = Master.query.filter_by(ipAddr=str(addr)).first()
            master = Master.query.filter_by(ipAddr='192.168.0.2').first()

            if master is None:
                print('등록 되지 않은 주소입니다.')
                client_socket.send('등록 되지 않은 주소입니다.'.encode('utf-8'))
                client_socket.close()
                continue

            sockNode_list_mutex.acquire()
            socketNode_list.append(socketNode(client_socket, addr))
            sockNode_list_mutex.release()

            client_thread = Thread(target=clientSocketStart, args=(client_socket, master))
            client_thread.start()

    except KeyboardInterrupt:
        print('소켓 서버 종료')
        server_socket.close()


def clientSocketStart(client_socket, master):
    print('clientSocketStart 쓰레드 생성 완료')
    client_socket.send('clientSocketStart 쓰레드 생성 완료'.encode('utf-8'))

    for node in socketNode_list:
        if node.client_sock is client_socket:
            print("클라이언트 소켓 리스트랑 스레드에 넣은 쓰레드가 동일하다.")
            manage_socketNode = node
            break
    else: # ecception
        print('에러남')


    while True:
        manage_socketNode.mutex.acquire()

        if manage_socketNode.newData:
            print('client: new data 있다.')
            manage_socketNode.sendData()

        manage_socketNode.mutex.release()


def checkChangeMaster():
    print('checkChangeMaster 쓰레드 생성 완료')

    while True:
        ###################################################
        masters = Master.query.filter_by(newdata=1).all()
        ###################################################
        # print("masters :", masters)
        # print("sock list:", socketNode_list)

        sockNode_list_mutex.acquire()

        for master in masters:
            manage_node = None
            for node in socketNode_list:
                # print('node.client :', str(node.client_addr[0]), " master.ipAddr :", master.ipAddr)

                if str(node.client_addr[0]) == master.ipAddr:
                    print('둘이 같음')
                    manage_node = node
                    break
            if manage_node is None:
                continue

            print('Master의 DB가 바뀜')

            manage_node.mutex.acquire()
            slaves = Slave.query.filter_by(master_id=master.id, newdata=1).all()

            RXAddr_list = []
            states_list = []

            for slave in slaves:
                RXAddr_list.append(slave.RXAddr)
                states_list.append(slave.state)

            manage_node.updateSlaveInfo(len(RXAddr_list), RXAddr_list, states_list)
            manage_node.newData = 1

            master.newdata = 0

            db.session.add(master)

            for slave in slaves:
                slave.newdata = 0
                db.session.add(slave)

            db.session.commit()

            manage_node.mutex.release()

        sockNode_list_mutex.release()


def sendToMaster(client_socket, data):
    data_json = json.dumps(data).encode('utf-8')
    client_socket.sendall(data_json)