import socket
import ollama
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Define the FastAPI app
app = FastAPI()

# Chat history to store the conversation
chat_history = []

# IP and Port for the server
host = '127.0.0.1'  # Localhost since frontend and backend are on the same machine
port = 42424

# Set up the socket connection
s = socket.socket()
s.bind((host, port))
s.listen(1)
print(f"Server started on {host}:{port}")

# Accept the connection
c, addr = s.accept()
print(f"Connection accepted from {addr}")

# Define the model for the message
class Message(BaseModel):
    message: str

@app.get("/get_chat")
async def get_chat():
    # Return the chat history
    return JSONResponse(content=chat_history)

@app.post("/send_message")
async def send_message(message: Message):
    # Retrieve the message from the POST request
    user_message = message.message

    # Add AI-1 message to chat history
    chat_history.append({"sender": "AI-1", "message": user_message})

    # OLLAMA AI interaction
    ai_response = ollama.chat(model="openhermes", messages=[{
        "role": 'user',
        "content": user_message,
    }])

    if 'message' in ai_response and 'content' in ai_response['message']:
        response = ai_response['message']['content']
    else:
        response = "Sorry, I couldn't process that."

    # Add AI-2 message to chat history
    chat_history.append({"sender": "AI-2", "message": response})

    # Send the response back to the client
    c.send(response.encode())
    print(f"Sent to AI-1: {response}")

    return JSONResponse(content={"response": response})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)