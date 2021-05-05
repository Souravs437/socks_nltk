import socket

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
HEADER = 64
DISCONNECT = '!D'
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def receive():
    message = client.recv(2048).decode(FORMAT)
    return message


def send(message):
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message.encode(FORMAT))


def start():
    while True:
        message = input()
        send(message)
        if message == DISCONNECT:
            print(receive())
            break
        else:
            print(receive())


start()