import socket
import ollama

# IP ADDRESS
host = '192.168.172.85'
# PORT
port = 4001

s = socket.socket()
s.bind((host, port))
print(f"\033[92mServer started on {host}:{port}\033[0m")
s.listen(1)
c, addr = s.accept()
print(f"\033[92mConnection accepted from {addr}\033[0m")

while True:
    # Receiving the message from the client
    data = c.recv(1024).decode()
    if not data:
        print("\033[91mNo data received. Closing connection.\033[0m")
        break
    print(f"\033[94mReceived from AI-1: {data}\033[0m\n")
    
    # OLLAMA AI interaction
    message = data
    ai_response = ollama.chat(model="openhermes", messages=[{
        "role": 'user',
        "content": message,
    }])

    if 'message' in ai_response and 'content' in ai_response['message']:
        response = ai_response['message']['content']
    else:
        response = "\033[91mSorry, I couldn't process that.\033[0m"

    # Sending the AI response to the client
    c.send(response.encode())
    print(f"\033[94mSent to AI-1: {response}\033[0m\n")

c.close()
print("\033[91mConnection closed.\033[0m")