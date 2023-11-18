import json
import socket
import threading


class StateServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.clients = {}  # Dictionary to store client addresses
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
        self.sock.bind((self.ip, self.port))  # Bind the socket to the server IP and port

    def start(self):
        print(f"Server started on {self.ip}:{self.port}")

        # Listen for incoming requests
        while True:
            data, address = self.sock.recvfrom(self.port)  # Receive data from a client

            # Create a thread to handle the request asynchronously
            thread = threading.Thread(target=self.handle_request, args=(self.sock, data, address))
            self.add_client(address)
            thread.start()

    def handle_request(self, sock, request, address):
        # Decode the data received
        request_data = json.loads(request.decode())

        print(f"Received request from {address}: {request_data}")

        # Process the request and update the server state

        # In this example, we simply broadcast the received request to all clients
        self.broadcast(json.dumps(request_data).encode())

    def broadcast(self, data):
        # Send data to all connected clients
        for client_address in self.clients.keys():
            print(f"Sending to {client_address}")
            self.sock.sendto(data, client_address)

    def add_client(self, address):
        if address in self.clients.keys():
            return
        # Add a new client to the server's client dictionary
        self.clients[address] = ''
        print(f"New client connected: {address}")

        # Send a welcome message to the new client
        welcome_message = f"Welcome {address} to the server!"
        self.broadcast(welcome_message.encode())

    def remove_client(self, client_id):
        # Remove a client from the server's client dictionary
        del self.clients[client_id]
        print(f"Client disconnected: {client_id}")

    # Rest of the code...


if __name__ == '__main__':
    # Server configuration
    SERVER_IP = "127.0.0.1"  # Replace with the actual server IP address
    SERVER_PORT = 9234  # Replace with the actual server port number

    # Create a StateServer instance
    server = StateServer(SERVER_IP, SERVER_PORT)

    # Start the server
    server.start()
