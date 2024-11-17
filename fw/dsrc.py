import serial
import time
import socket
import threading

class ToDoApp:
    def __init__(self, server_ip, server_port, skip_login):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = None
        self.skip_login = skip_login

        SERIAL_PORT = 'COM5'    # Replace with the actual port for your ESP32
        BAUD_RATE = 115200      # Same baud rate as in your ESP32 code
        # Open the serial port
        self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)


    def display_menu(self):
        print("\n--- DSRC App ---")
        print("1. Enable the RSU 1")
        print("2. Disiable the RSU 2")
        print("3. Get Status RSU 3")
        print("4. Open Gate 4")
        print("5. Close Gate 5")
        print("10. Exit")

    def command1(self):
        print("Executing: enable the RSU")

    def command2(self):
        print("Executing: disable the RSU")

    def command3(self):
        print("Executing get status RSU")

    def handle_server_data(self):
        """ Continuously listen for server messages and print them. """
        while True:
            try:
                data = self.socket.recv(1024)  # Read data from the server
                if data:
                    print(f"Received from server: {data.decode()}")
                else:
                    print("Connection closed by the server.")
                    break
            except Exception as e:
                print(f"Error receiving data: {e}")
                break

    def connect_to_server(self):
        """ Establish connection to the server. """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.server_port))
            print(f"Connected to {self.server_ip}:{self.server_port}")

            # Start a thread to handle incoming server data
            threading.Thread(target=self.handle_server_data, daemon=True).start()

        except Exception as e:
            print(f"Error connecting to server: {e}")

    def login(self):
        """ Simulate a simple login (could be extended to ask for a username/password). """
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Send login credentials to the server
        login_message = f"LOGIN {username} {password}"
        self.socket.send(login_message.encode())
        print(f"Sent login credentials for {username}.")

    def send_data_to_server(self, message):
        """ Send data to the server. """
        if self.socket:
            self.socket.send(message.encode())
        else:
            print("No server connection.")

    def send_command(self,command):
        print(f"Sending: {command}")
        self.ser.write(command.encode())  # Send the command to the serial port

    def run(self):
        if self.skip_login == True:
            self.connect_to_server()
            self.login()

        #configure the timing
        self.send_command("open_time 200\n")
        self.send_command("close_time 200\n")


        while True:
            self.display_menu()
            choice = input("Select an option (1-4): ")

            if choice == "1":
                self.command1()
            elif choice == "2":
                self.command2()
            elif choice == "3":
                self.command3()
            elif choice == "4":
                self.send_command("open\n")
            elif choice == "5":
                self.send_command("close\n")                
            elif choice == "10":
                print("Exiting the app. Goodbye!")
                self.socket.close()  # Close the socket when exiting
                break
            else:
                print("Invalid choice. Please select a number between 1 and 4.")

if __name__ == "__main__":
    # Set the server IP and port
    print("Starting")
    server_ip = '127.0.0.1'  # Replace with your server's IP address
    server_port = 12345       # Replace with your server's port number

    # Wait a moment to ensure the ESP32 is ready
    time.sleep(2)

    app = ToDoApp(server_ip, server_port, False)
    app.run()
