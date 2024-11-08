// pages/api/chat.js
export default async function handler(req, res) {
    if (req.method === 'POST') {
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(req.body),
        });
        const data = await response.json();
        res.status(200).json(data);
    } else if (req.method === 'GET') {
        const response = await fetch('http://localhost:8000/chat');
        const data = await response.json();
        res.status(200).json(data);
    }
}
