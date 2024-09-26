import socket
import ollama

# IP address
host = '192.168.14.245'  
# PORT
port = 8750

s = socket.socket()
s.connect((host, port))

print(f"Connected to server at {host}:{port}")

# First message
message = "Hey, how are you"

while True:

    print(f"Sending to AI-2: {message}\n")
    s.send(message.encode())

    # Receiving response from the server
    data = s.recv(1024).decode()
    print(f"Received from AI-2: {data}\n")

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