import serial
import time
import socket
import threading

# Specify your serial port (update COMx with your actual port)
SERIAL_PORT = 'COM5'    # Replace with the actual port for your ESP32
BAUD_RATE = 115200      # Same baud rate as in your ESP32 code

# Open the serial port
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def send_command(command):
    print(f"Sending: {command}")
    ser.write(command.encode())  # Send the command to the serial port

# Wait a moment to ensure the ESP32 is ready
time.sleep(2)


#configure the timing
send_command("open_time 200\n")
send_command("close_time 200\n")

while(1):
    send_command("open\n")
    time.sleep(1)
    send_command("close\n")
    time.sleep(1)    

# Close the serial port
ser.close()
