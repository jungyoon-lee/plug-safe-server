import json
from socket import *
from threading import Thread

from app.models.device import temp_master, Master, Slave
from app import db

from app.routes.device import bytes_to_dict

port = 8081

def server_start():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('0.0.0.0', port))
    serverSocket.listen(1)

    print('포트 번호 %d 사용 중' % port)

    clientSocket, addr = serverSocket.accept()
    print(str(addr), '에서 접속되었습니다.')

    while True:
        recv_data = clientSocket.recv(1024)
        print('server: ', recv_data.decode('utf-8'))

        send_data = 'lets hadnshake with me'
        clientSocket.send(send_data.encode('utf-8'))

    clientSocket.close()


def check_change_master(master):

    while True:
        if master.newdata is True:
            slaves = Slave.query.filter_by(master_id=master.id, newdata=1).all()





def send_to_master(clientSocket, data):
    data_json = json.dumps(data).encode('utf-8')
    clientSocket.sendall(data_json)