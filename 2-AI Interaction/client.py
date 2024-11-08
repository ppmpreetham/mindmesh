import socket
import ollama

# ANSI escape codes for colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'

# IP address
host = '192.168.137.1'  
# PORT
port = 8750

s = socket.socket()
s.connect((host, port))

print(f"{GREEN}Connected to server at {host}:{port}{RESET}")

# First message
message = "Hey, how are you"

while True:

    print(f"{CYAN}Sending to AI-2: {message}{RESET}\n")
    s.send(message.encode())

    # Receiving response from the server
    data = s.recv(1024).decode()
    print(f"{YELLOW}Received from AI-2: {data}{RESET}\n")

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

    print(f"{MAGENTA}AI response: {message}{RESET}")

s.close()
print(f"{RED}Connection closed.{RESET}")