import json
import socket
import time
import threading


class UDPClient:
    def __init__(self, server_ip, server_port):
        self.client_port = 9235  # Replace with the actual client port number
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 9235))  # Bind to any available local address and port
        self.lock = threading.Lock()

    def send_data(self, data):
        try:
            # Serialize the data to JSON
            serialized_data = json.dumps(data)
            # Send the serialized data to the server
            self.sock.sendto(serialized_data.encode(), (self.server_ip, self.server_port))
        except Exception as e:
            print("An error occurred during data transmission:", e)

    def receive_response(self):
        try:
            while True:
                # Receive the response from the server
                response, address = self.sock.recvfrom(self.client_port)
                response_data = json.loads(response.decode())
                # Print the response received from the server
                print(f"Response: {response_data} from server: {address}")

        except Exception as e:
            print("An error occurred during response reception:", e)

    def start(self):
        # Start a thread to receive responses from the server
        response_thread = threading.Thread(target=self.receive_response)
        response_thread.start()

        # Send data to the server every 4 seconds
        while True:
            # Create an object to send
            data = {
                "name": "John",
                "age": 30,
                "city": "New York"
            }

            # Acquire a lock to ensure thread safety
            self.lock.acquire()

            # Send the object to the server
            self.send_data(data)

            # Release the lock
            self.lock.release()

            # Sleep for 4 seconds before sending the next object
            time.sleep(4)


def main():
    # Server configuration
    server_ip = "127.0.0.1"  # Replace with the actual server IP address
    server_port = 9234  # Replace with the actual server port number

    # Create a UDP client instance
    client = UDPClient(server_ip, server_port)

    # Start the client
    client.start()


if __name__ == '__main__':
    main()
