import requests

# Define the URL
url = 'http://10.0.1.155/startrf'

# Define any data you want to send with the POST request (optional)
# You can pass data in various formats such as JSON, form-encoded, etc.
data = {
    'key1': 'value1',  # Example form data
    'key2': 'value2'
}

# Optionally, you can send headers (e.g., for content type, authentication)
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'  # or 'application/json' if needed
}

# Send the POST request
response = requests.post(url, data=data, headers=headers)

# Print the response status code and content
print(f"Status Code: {response.status_code}")
print(f"Response Content: {response.text}")
