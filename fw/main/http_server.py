import http.server
import socketserver
import urllib.parse

# Define the IP and Port for the server
HOST = '0.0.0.0'  # Your server IP
PORT = 8088  # Port to listen on

# Custom request handler to handle POST data
class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the length of the data
        content_length = int(self.headers['Content-Length'])
        
        # Read the data from the client
        post_data = self.rfile.read(content_length)
        
        # Print the data to the console (decoded)
        print(f"Received data: {post_data.decode('utf-8')}")
        
        # Send a response back to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Data received successfully")

# Set up the server with a specific IP and port
with socketserver.TCPServer((HOST, PORT), MyRequestHandler) as httpd:
    print(f"Serving HTTP on {HOST}:{PORT}...")
    httpd.serve_forever()
