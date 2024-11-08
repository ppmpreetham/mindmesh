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
        body { font-family: Arial, sans-serif; display: flex; flex-direction: column; align-items: center; background: #2c2c2c;}
        .container { width: 100%; max-width: 600px; margin-top: 0px; }
        .message {border-radius: 10px; margin-bottom: 10px; padding: 10px; }

        .received { background-color: #e1f5fe; align-self: flex-start; text-align: left; }
        .sent { background-color: #c8e6c9; align-self: flex-end; text-align: right; }

    </style>
</head>
<body>
    <h2>AI Chat Interaction</h2>
    <div class="container" id="messages"></div>

    <script>
        const ws = new WebSocket("ws://localhost:8000/ws");

        ws.onmessage = function(event) {
            const messages = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', 'received');
            messageDiv.textContent = event.data;
            messages.appendChild(messageDiv);
            applyAlternateColor();
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
                applyAlternateColor();
            }
        }

        function applyAlternateColor() {
            const messages = document.getElementById('messages').children;
            for (let i = 0; i < messages.length; i++) {
                if (i % 2 === 1) {
                    messages[i].style.background = '#005c4b';
                    messages[i].style.color = 'white';
                    messages[i].style.alignSelf = 'flex-start';
                    messages[i].style.textAlign = 'right';
                } else {
                    messages[i].style.color = 'white';
                    messages[i].style.background = '#363636';
                    messages[i].style.alignSelf = 'flex-end';
                    messages[i].style.textAlign = 'left';
                }
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