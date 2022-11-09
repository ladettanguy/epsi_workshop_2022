import socket
import threading


class Log:
    sock: socket.socket = None

    @staticmethod
    def log(message: str):
        print(message)
        if Log.sock is None:
            return
        Log.sock.send(message.encode("utf-8"))


log_socker = socket.socket()
host = '127.0.0.1'
port = 7777
try:
    log_socker.bind((host, port))
except socket.error as e:
    print(str(e))


def wait_connection():
    while True:
        Log.sock, address = log_socker.accept()
        while True:
            data = Log.sock.recv(2048)
            if not data:
                Log.sock = None
                break


log_socker.listen(1)
t = threading.Thread(target=wait_connection)
t.start()
