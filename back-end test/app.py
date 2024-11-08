from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import ollama
import uvicorn
import socket

app = FastAPI()

# HTML template to render the UI
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chat Interaction</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; flex-direction: column; align-items: center; }
        .container { width: 90%; max-width: 600px; margin-top: 20px; }
        .message { padding: 10px; border-radius: 10px; margin-bottom: 10px; max-width: 70%; }
        .received { background-color: #e1f5fe; align-self: flex-start; }
        .sent { background-color: #c8e6c9; align-self: flex-end; }
        .input-container { display: flex; width: 100%; }
        .input-container input { flex-grow: 1; padding: 10px; font-size: 16px; }
        .input-container button { padding: 10px 20px; font-size: 16px; }
    </style>
</head>
<body>
    <h2>AI Chat Interaction</h2>
    <div class="container" id="messages"></div>
    <div class="input-container">
        <input type="text" id="userInput" placeholder="Type your message..."/>
        <button onclick="sendMessage()">Send</button>
    </div>
    
    <script>
        const ws = new WebSocket("ws://localhost:8000/ws");

        ws.onmessage = function(event) {
            const messages = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', 'received');
            messageDiv.textContent = event.data;
            messages.appendChild(messageDiv);
        };

        function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value;
            if (message) {
                const messages = document.getElementById('messages');
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message', 'sent');
                messageDiv.textContent = message;
                messages.appendChild(messageDiv);
                ws.send(message);
                input.value = '';
            }
        }
    </script>
</body>
</html>
"""

host = '192.168.172.85'
port = 4001
s = socket.socket()
s.bind((host, port))
s.listen(1)
c, addr = s.accept()

# Serve the HTML page
@app.get("/")
async def get():
    return HTMLResponse(html)

# WebSocket endpoint for real-time chat
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Receive message from the client (AI-1)
        data = c.recv(1024).decode()
        await websocket.send_text(data)
        
        # Process message with ollama AI
        ai_response = ollama.chat(model="openhermes", messages=[{
            "role": 'user',
            "content": data,
        }])

        # Check if AI response contains the expected message content
        if 'message' in ai_response and 'content' in ai_response['message']:
            response = ai_response['message']['content']
        else:
            response = "Sorry, I couldn't process that."

        # Send AI response back to client
        c.send(response.encode())
        await websocket.send_text(response)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)