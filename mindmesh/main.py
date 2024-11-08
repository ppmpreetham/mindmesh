from fastapi import FastAPI
import socket
import ollama
from typing import List

app = FastAPI()

def connect_to_server():
    s = socket.socket()
    s.connect(('192.168.14.245', 42424))
    return s

@app.post("/start-conversation/")
async def start_conversation(initial_message: str):
    # Step 1: Send the initial message to the server (AI-2)
    conversation = []
    conversation.append(f"Sending to AI-2: {initial_message}")

    with connect_to_server() as server_socket:
        server_socket.send(initial_message.encode())
        response = server_socket.recv(1024).decode()

    conversation.append(f"Received from AI-2: {response}")

    # Step 2: AI-1 sends the message to AI-2 and gets a response
    ai_response = ollama.chat(
        model="openhermes",
        messages=[{"role": 'user', "content": response}],
    )
    if 'message' in ai_response and 'content' in ai_response['message']:
        ai_message = ai_response['message']['content']
    else:
        ai_message = "Sorry, I couldn't process that."

    conversation.append(f"AI response: {ai_message}")
    return {"conversation": conversation}