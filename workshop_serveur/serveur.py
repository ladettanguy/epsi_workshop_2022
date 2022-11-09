import socket
import sys

from thread_client import Client

ServerSocket = socket.socket()
port = int(sys.argv[1])
try:
    ServerSocket.bind(("", port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)

while True:
    sock, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    Client(sock, address).start()
ServerSocket.close()
