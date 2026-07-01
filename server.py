import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

# Store connected clients and nicknames
clients = []
nicknames = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen()
print("Server started...")
print(f"Listening on {HOST}:{PORT}")
# Send message to all clients
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass

# Handle each connected client
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                raise Exception()
            broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                nickname = nicknames[index]
                nicknames.remove(nickname)

                client.close()

                broadcast(
                    f"{nickname} left chat room".encode()
                )
                print(f"{nickname} disconnected")
            break
# Receive clients
def receive():
    while True:
        client, address = server.accept()
        print("Connected with:", address)

        # Ask for nickname
        client.send("NICK".encode())
        nickname = client.recv(1024).decode()
        clients.append(client)
        nicknames.append(nickname)
        print(f"Nickname: {nickname}")

        broadcast(
            f"{nickname} joined the chat room".encode()
        )
        client.send(
            "Connected to server!".encode()
        )
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()