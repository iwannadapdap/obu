import socket

# Define the server IP and port
HOST = '10.0.1.100'  # IP address of the server
PORT = 8088  # Port number to listen on

def start_server():
    # Create a socket (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server's address and port
    server_socket.bind((HOST, PORT))

    # Start listening for incoming connections (max 5 queued connections)
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}...")

    while True:
        # Accept incoming connections
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        try:
            # Receive data in chunks (e.g., 1024 bytes at a time)
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break  # No more data, connection closed by client

                # Process the incoming data (you can parse it as needed)
                print(f"Received data: {data.decode('utf-8')}")

                # Optionally, send a response back to the client
                response = "Data received successfully"
                client_socket.sendall(response.encode('utf-8'))

        except Exception as e:
            print(f"Error while receiving data: {e}")

        finally:
            # Close the client socket
            client_socket.close()
            print("Connection closed")

if __name__ == "__main__":
    start_server()
