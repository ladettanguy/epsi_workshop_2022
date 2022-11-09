import signal
import socket
import sys

from thread_client import Client

ServerSocket = socket.socket()
port = int(sys.argv[1])
try:
    ServerSocket.bind(("", port))
except socket.error as e:
    print(str(e))


def handler(_, __):
    ServerSocket.close()
    exit(0)


signal.signal(signal.SIGINT, handler)

print('Waiting for a Connection..')
ServerSocket.listen(5)

while True:
    sock, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    Client(sock, address).start()
