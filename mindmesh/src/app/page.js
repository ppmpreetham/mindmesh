// pages/index.js
"use client"
import { useEffect, useState } from 'react';

export default function Home() {
    const [chat, setChat] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        // Load initial chat
        fetchChat();
    }, []);

    const fetchChat = async () => {
        const response = await fetch('/api/chat');
        const data = await response.json();
        setChat(data);
    };

    const sendMessage = async () => {
        setLoading(true);
        await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sender: "AI 1", text: "Hello from AI 1" }),
        });
        fetchChat();
        setLoading(false);
    };

    return (
        <div>
            <h1>AI Chat</h1>
            <div style={{ border: '1px solid #ddd', padding: '10px', maxHeight: '300px', overflowY: 'scroll' }}>
                {chat.map((msg, index) => (
                    <div key={index}>
                        <strong>{msg.sender}:</strong> {msg.text}
                    </div>
                ))}
            </div>
            <button onClick={sendMessage} disabled={loading}>Send Message</button>
        </div>
    );
}
