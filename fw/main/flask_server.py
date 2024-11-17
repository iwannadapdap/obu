from flask import Flask, request

# Create a Flask application instance
app = Flask(__name__)

# Define a POST route to handle incoming data
@app.route('/postdata', methods=['POST'])
def handle_post_data():
    # Check if the incoming request is JSON
    if request.is_json:
        data = request.get_json()  # Parse JSON data
        print(f"Received JSON: {data}")
    else:
        # For non-JSON data, treat it as form-encoded or raw data
        data = request.data.decode('utf-8')  # Read raw data (as a string)
        print(f"Received data: {data}")
    
    # Send a response back to the client
    return "Data received successfully", 200

# Run the Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)

