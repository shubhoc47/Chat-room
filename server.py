import socket
import threading

PORT = 6699

SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def private_message(idx, message):
    print("print: ", len(nicknames), len(clients))
    clients[idx].send(message.encode(FORMAT))


def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            check_msg = msg.decode(FORMAT).split()
            print(check_msg)
            nk = check_msg[1][1:]

            if nk in nicknames:
                msg = check_msg[0] + " (PM) "
                msg += ' '.join(check_msg[2:])
                private_message(nicknames.index(nk), msg)
            else:
                broadcast(msg)

        except:
            if client in clients:
                idx = clients.index(client)
                print(client)

                clients.remove(client)
                client.close()
                broadcast(f'{nicknames[idx]} left the chat!'.encode(FORMAT))
                nicknames.remove(nicknames[idx])
            break


def start():
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        client.send('NICK'.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        clients.append(client)
        nicknames.append(nickname)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined!\n'.encode(FORMAT))
        client.send('Connected to the server!'.encode(FORMAT))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()
