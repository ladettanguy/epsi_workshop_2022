import socket

client_socket = socket.socket()
host = "127.0.0.1"
port = 7777

print('Waiting for connection response')
try:
    client_socket.connect((host, port))
except socket.error as e:
    print(str(e))
print("Connected !")

while True:
    data = client_socket.recv(2048)
    if not data:
        break
    print(data.decode("utf-8"))
client_socket.close()
