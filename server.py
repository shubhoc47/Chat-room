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

# Sending message to every clients connected to the server
def broadcast(message):
    for client in clients:
        client.send(message)


# Transmiting message to a specific client 
def private_message(idx, message):
    print("print: ", len(nicknames), len(clients))
    clients[idx].send(message.encode(FORMAT))


def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            check_msg = msg.decode(FORMAT).split()
            print(check_msg)
            nk = check_msg[1][1:] # Getting the second word from the array to check for Nick_Name

            
            if nk in nicknames and check_msg[1][0] == '@': # If anyone wants to send private message, he/she has to put "@name".
                msg = check_msg[0] + " (PM) " # The private message consists of the sender name followed by "(PM)" to alert the receiver that this is a private message
                msg += ' '.join(check_msg[2:])
                private_message(nicknames.index(nk), msg)
            else:
                broadcast(msg)

        except:
            if client in clients:
                idx = clients.index(client)
                print(client)

                clients.remove(client) # Removing client if it disconnects or any problem occures at the client end.
                client.close()
                broadcast(f'{nicknames[idx]} left the chat!'.encode(FORMAT)) # Notifing all clients with the name of the client who left the room.
                nicknames.remove(nicknames[idx]) # Removing the nickname of the leaving client as well.
            break


def start():
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        client.send('NICK'.encode(FORMAT)) # Whenever a new client joins the room, server sends a "NICK" message to provide a nick-name.
        nickname = client.recv(1024).decode(FORMAT)
        # When new client provides a nick-name, it's been added to client and nickname array.
        clients.append(client)
        nicknames.append(nickname)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined!\n'.encode(FORMAT)) # Broadcasting message to notify about new client.
        client.send('Connected to the server!'.encode(FORMAT))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()
