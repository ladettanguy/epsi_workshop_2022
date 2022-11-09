import socket
import sys
import threading

client_socket = socket.socket()
host, port = sys.argv[1].split(":")

print('Waiting for connection response')
try:
    client_socket.connect((host, int(port)))
except socket.error as e:
    print(str(e))

country = sys.argv[2]

client_socket.send(country.encode('utf-8'))


def user_input():
    user_data = input()
    client_socket.send(user_data.encode("utf-8"))


t1: threading.Thread = threading.Thread(target=user_input)
t1.start()

while True:
    data = client_socket.recv(2048)
    if not data:
        break
    print(data.decode('utf-8'))

t1.join(timeout=0)
client_socket.close()
