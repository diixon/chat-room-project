import socket
import threading


HOST = "127.0.0.1"
PORT = 5555

# Ask user for nickname
nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Receive messages
def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            # Server requests nickname
            if message == "NICK":
                client.send(nickname.encode())
            else:
                print(message)
        except:
            print("Receive Error")
            client.close()
            break

# Send messages
def write():
    while True:
        try:
            text = input()
            message = f"{nickname}: {text}"
            client.send(message.encode())
        except:
            print("Write Error")
            client.close()
            break

# Receive thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Write thread
write_thread = threading.Thread(target=write)
write_thread.start()