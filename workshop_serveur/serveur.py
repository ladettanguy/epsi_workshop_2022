import signal
import socket
import sys

from thread_client import Client
from logger.log import Log

ServerSocket = socket.socket()
port = int(sys.argv[1])
try:
    ServerSocket.bind(("", port))
except socket.error as e:
    print(str(e))


def handler(_, __):
    ServerSocket.close()
    Log.sock.close() if Log.sock else exit(1)
    exit(1)


signal.signal(signal.SIGINT, handler)

print('Waiting for a Connection..')
ServerSocket.listen(5)

while True:
    sock, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    Client(sock, address).start()
