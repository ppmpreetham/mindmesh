import requests
import ollama

message="how are you doing?"

response = ollama.chat(model="openhermes", messages=[
    {
    "role":'user',
    "content": message,
    },
])

print(response['message']['content'])