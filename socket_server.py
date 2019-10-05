import json
from socket import *
from threading import Thread, Lock
from queue import Queue

from app.models.device import Master, Slave
from app import session

myqueue = Queue(10)

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
        self.newData = False
        self.changes = False
        self.RXAddr = []
        self.states = []

    def updateSlaveInfo(self, changes, RXAddr_list, states_list):
        print('updateSlaveInfo')
        self.changes = changes
        self.RXAddr = RXAddr_list
        self.states = states_list
        self.newData = True

    def sendData(self):
        sign = False
        if self.newData:
            data = {'changes': self.changes, 'slaves_addr': self.RXAddr, 'states': self.states}

            print(data)
            data_json = json.dumps(data).encode('utf-8')
            self.client_sock.sendall(data_json)
            self.newData = False
            sign = True

        return sign


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
            db_session = session()

            client_socket, addr = server_socket.accept()
            print(str(addr), '에서 접속되었습니다.')

            print(addr[0])
            master = db_session.query(Master).filter(Master.ipAddr == str(addr[0])).first()

            if master is None:
                print('등록 되지 않은 주소입니다.')
                client_socket.send('등록 되지 않은 주소입니다.'.encode('utf-8'))
                client_socket.close()
                db_session.close()
                continue

            flag = False
            for node in socketNode_list:
                if node.client_addr[0] is addr[0]:
                    node.mutex.acquire()
                    print("기존 노드 소켓 갱신")
                    node.client_sock.close()
                    node.client_sock = client_socket
                    node.client_addr = addr
                    node.mutex.release()
                    flag = True
                    break
            if flag:
                db_session.close()
                continue



            sockNode_list_mutex.acquire()
            socketNode_list.append(socketNode(client_socket, addr))
            sockNode_list_mutex.release()

            client_thread = Thread(target=clientSocketStart, args=(client_socket, master))
            client_thread.start()

            db_session.close()

    except KeyboardInterrupt:
        print('소켓 서버 종료')
        server_socket.close()


def clientSocketStart(client_socket, master):
    print('clientSocketStart 쓰레드 생성 완료')
    client_socket.send('clientSocketStart 쓰레드 생성 완료'.encode('utf-8'))

    for node in socketNode_list:
        if node.client_sock is client_socket:
            manage_socketNode = node
            break
    else: # ecception
        print('에러남')

    while True:
        manage_socketNode.mutex.acquire()

        if manage_socketNode.newData:
            manage_socketNode.sendData()

        manage_socketNode.mutex.release()


def checkChangeMaster():
    #print('checkChangeMaster 쓰레드 생성 완료')

    while True:
        myqueue.get()
        db_session = session()

        masters = db_session.query(Master).filter(Master.newdata == 1).all()

        for master in masters:
            slaves = db_session.query(Slave).filter(Slave.master_id == master.id, Slave.newdata == 1).all()
            for slave in slaves:
                print(slave, slave.newdata, slave.state)

        sockNode_list_mutex.acquire()

        for master in masters:
            manage_node = None
            for node in socketNode_list:
                # print('node.client :', str(node.client_addr[0]), " master.ipAddr :", master.ipAddr)

                if str(node.client_addr[0]) == master.ipAddr:
                    manage_node = node
                    break
            if manage_node is None:
                continue

            manage_node.mutex.acquire()

            slaves = db_session.query(Slave).filter(Slave.master_id == master.id, Slave.newdata == 1).all()

            RXAddr_list = []
            states_list = []

            for slave in slaves:
                RXAddr_list.append(slave.RXAddr)
                states_list.append(slave.state)

            manage_node.updateSlaveInfo(len(RXAddr_list), RXAddr_list, states_list)
            manage_node.newData = 1

            master.newdata = 0

            db_session.add(master)
            db_session.commit()

            for slave in slaves:
                slave.newdata = 0
                db_session.add(slave)
                db_session.commit()

            manage_node.mutex.release()

        db_session.close()
        sockNode_list_mutex.release()
