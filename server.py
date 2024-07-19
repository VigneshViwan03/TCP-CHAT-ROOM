import socket
import threading

# List to keep track of connected clients
clients = []
nicknames = []

# Function to broadcast messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle each client connection
def handle(client):
    while True:
        try:
            # Receive message from client
            message = client.recv(1024)
            broadcast(message)
        except:
            # If an error occurs, remove and close the client connection
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

# Function to receive new connections
def receive():
    while True:
        # Accept connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request and store nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print and broadcast nickname
        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        # Start handling thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Set up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 55555))
server.listen()
print("Server is listening on 127.0.0.1:55555")

# Start receiving connections
receive()

