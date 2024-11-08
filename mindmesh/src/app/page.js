// pages/index.js
"use client"
import { useEffect, useState } from 'react';

export default function Page() {
    const [chat, setChat] = useState([]);
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);

    // Fetch the chat history when the component mounts
    useEffect(() => {
        fetchChat();
    }, []);

    // Fetch chat history from the FastAPI server
    const fetchChat = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/get_chat');
            const data = await response.json();
            setChat(data);
        } catch (error) {
            console.error('Error fetching chat:', error);
        }
    };

    // Send a message to the server
    const sendMessage = async () => {
        if (!message.trim()) return;

        setLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:5000/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            const data = await response.json();
            setChat([
                ...chat,
                { sender: 'AI 1', message }, 
                { sender: 'AI 2', message: data.response }
            ]);
            setMessage("");
        } catch (error) {
            console.error('Error sending message:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>AI Chat</h1>
            <div
                style={{
                    border: '1px solid #ddd',
                    padding: '10px',
                    maxHeight: '300px',
                    overflowY: 'scroll',
                    marginBottom: '10px',
                }}
            >
                {chat.map((msg, index) => (
                    <div key={index}>
                        <strong>{msg.sender}:</strong> {msg.message}
                    </div>
                ))}
            </div>
            <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type your message..."
                style={{ width: '80%', padding: '8px', marginRight: '10px' }}
            />
            <button onClick={sendMessage} disabled={loading} style={{ padding: '8px 12px' }}>
                {loading ? 'Sending...' : 'Send'}
            </button>
        </div>
    );
}