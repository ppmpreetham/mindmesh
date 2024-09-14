import socket
import ollama

# IP address
host = '192.168.73.187'  
# PORT
port = 42424

s = socket.socket()
s.connect((host, port))

print(f"Connected to server at {host}:{port}")

# First message
message = "Hey, I find you cute and want to talk to you"

while True:

    print(f"Sending to server: {message}")
    s.send(message.encode())

    # Receiving response from the server
    data = s.recv(1024).decode()
    print(f"Received from server: {data}")

    if message.lower().strip() == 'bye' or data.lower().strip() == 'bye':
        break

    # client response based on the received message
    ai_response = ollama.chat(model="openhermes", messages=[{
        "role": 'user',
        "content": data,
    }])
    
    if 'message' in ai_response and 'content' in ai_response['message']:
        message = ai_response['message']['content']
    else:
        message = "Sorry, I couldn't process that."

    print(f"AI response: {message}")

s.close()
print("Connection closed.")