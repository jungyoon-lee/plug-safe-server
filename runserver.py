from multiprocessing import Process

from app import app
from socket_server import server_start

host = '0.0.0.0'
server_port = 8080
socket_port = 8081

# if __name__ == '__main__':
#     processes = []
#
#     socket = Process(target=server_start, args=())
#     http = Process(target=app.run, args=(host, server_port))
#
#     processes.append(socket)
#     processes.append(http)
#
#     socket.start()
#     http.start()

if __name__ == '__main__':
    app.run(host=host, port=server_port)