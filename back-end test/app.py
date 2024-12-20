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
        body { font-family: Arial, sans-serif; display: flex; flex-direction: column; align-items: center; background-image: url('https://raw.githubusercontent.com/ppmpreetham/mindmesh/refs/heads/main/back-end%20test/background.png');}
        .container { width: 100%; max-width: 600px; margin-top: 0px; }
        .message { border-radius: 10px; margin-bottom: 5px; padding: 10px; }

        .received { background-color: #e1f5fe; align-self: flex-start; text-align: left; }
        .sent { background-color: #c8e6c9; align-self: flex-end; text-align: right; }

        .theme-selector { position: absolute; top: 10px; right: 10px; }
    </style>
</head>
<body>
    <h2 style="color:white">AI Chat Interaction</h2>
    <div class="theme-selector">
        <label for="theme">Select Theme:</label>
        <select id="theme" onchange="changeTheme()">
            <option value="whatsapp">Whatsapp</option>
            <option value="retro">Retro</option>
            <option value="love">Love Theme</option>
        </select>
    </div>
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

        function changeTheme() {
            const theme = document.getElementById('theme').value;
            const messages = document.getElementsByClassName('message');
            if (theme === 'whatsapp') {
                document.body.style.backgroundColor = '#f0f0f0';
                document.body.style.color = 'white';
                document.body.style.backgroundImage = "url('https://raw.githubusercontent.com/ppmpreetham/mindmesh/refs/heads/main/back-end%20test/background.png')";
                for (let message of messages) {
                    if (message.classList.contains('received')) {
                        message.style.backgroundColor = '#e1f5fe';
                    } else {
                        message.style.backgroundColor = '#c8e6c9';
                    }
                }
            } else if (theme === 'retro') {
                document.body.style.backgroundColor = '#f5ecdb';
                document.body.style.backgroundImage = "url('https://raw.githubusercontent.com/ppmpreetham/mindmesh/refs/heads/main/back-end%20test/biege.png')";
                document.body.style.color = '#74c6ef';
                for (let message of messages) {
                    if (message.classList.contains('received')) {
                        message.style.backgroundColor = '#e1f5fe';
                    } else {
                        message.style.backgroundColor = '#c8e6c9';
                    }
                }
            } else if (theme === 'love') {
                document.body.style.backgroundImage = "url('https://raw.githubusercontent.com/ppmpreetham/mindmesh/refs/heads/main/back-end%20test/wallpaper2you_40542.jpg')";
                document.body.style.backgroundColor = '#ffffff';
                document.body.style.color = 'black';
                for (let message of messages) {
                    if (message.classList.contains('received')) {
                        message.style.backgroundColor = '#ffcccb';
                    } else {
                        message.style.backgroundColor = '#ffb6c1';
                    }
                }
            } else {
                document.body.style.backgroundColor = '';
                document.body.style.color = '';
                document.body.style.backgroundImage = '';
                for (let message of messages) {
                    if (message.classList.contains('received')) {
                        message.style.backgroundColor = '#e1f5fe';
                    } else {
                        message.style.backgroundColor = '#c8e6c9';
                    }
                }
            }
        }
    </script>
</body>
</html>
"""

host = '192.168.172.231'
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