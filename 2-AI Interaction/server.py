import socket
import ollama

#IP ADDRESS
host = '192.168.73.187'
#PORT
port = 42424

s = socket.socket()
s.bind((host, port))
print(f"Server started on {host}:{port}")
s.listen(1)
c, addr = s.accept()
print(f"Connection accepted from {addr}")

while True:
    # Receiving the message from the client
    data = c.recv(1024).decode()
    if not data:
        print("No data received. Closing connection.")
        break
    print(f"Received from client: {data}")
    
    # OLLAMA AI interaction
    message = data
    ai_response = ollama.chat(model="openhermes", messages=[{
        "role": 'user',
        "content": message,
    }])

    if 'message' in ai_response and 'content' in ai_response['message']:
        response = ai_response['message']['content']
    else:
        response = "Sorry, I couldn't process that."

    # Sending the AI response to the client
    c.send(response.encode())
    print(f"Sent to client: {response}")

c.close()
print("Connection closed.")
