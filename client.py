import socket
import threading

PORT = 6699

SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

nickname = input("Enter a nickname: ")


def receive():
    while True:
        try:
            mess = client.recv(1024).decode(FORMAT)
            if mess == 'NICK':
                client.send(nickname.encode(FORMAT))
            else:
                print(mess)
        except:
            print("Error occurred!")


def write():
    while True:
        mess = f'{nickname}: {input()}'
        client.send(mess.encode(FORMAT))


def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
