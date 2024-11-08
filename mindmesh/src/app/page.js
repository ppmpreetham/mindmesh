"use client";
import React, { useState, useEffect, useRef } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { MessageSquare } from 'lucide-react';

const AIChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [initialMessage, setInitialMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isStarted, setIsStarted] = useState(false);
  const ws = useRef(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const connectWebSocket = () => {
    ws.current = new WebSocket('ws://192.168.137.1:8000/ws/chat');
    
    ws.current.onopen = () => {
      setIsConnected(true);
      console.log('Connected to WebSocket');
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.message) {
        setMessages((prevMessages) => [...prevMessages, { speaker: 'AI-1', message: data.message }]);
      }
      if (data.error) {
        console.error('Error:', data.error);
      }
    };

    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.current.onclose = () => {
      setIsConnected(false);
      console.log('Disconnected from WebSocket');
    };
  };

  const startConversation = () => {
    if (ws.current && initialMessage) {
      ws.current.send(JSON.stringify({ message: initialMessage }));
      setMessages((prevMessages) => [...prevMessages, { speaker: 'User', message: initialMessage }]);
      setIsStarted(true);
    }
  };

  useEffect(() => {
    connectWebSocket();
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  return (
    <Card className="w-full max-w-2xl mx-auto my-8">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MessageSquare className="w-6 h-6" />
          AI Conversation Viewer
        </CardTitle>
      </CardHeader>
      <CardContent>
        {!isStarted ? (
          <div className="space-y-4">
            <Input
              type="text"
              placeholder="Enter initial message to start the conversation..."
              value={initialMessage}
              onChange={(e) => setInitialMessage(e.target.value)}
              className="w-full"
            />
            <Button
              onClick={startConversation}
              disabled={!isConnected || !initialMessage.trim()}
              className="w-full"
            >
              Start Conversation
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="h-96 overflow-y-auto space-y-4 p-4 border rounded-lg">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${
                    msg.speaker === 'AI-1' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-[80%] p-3 rounded-lg ${
                      msg.speaker === 'AI-1'
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    <div className="text-xs font-semibold mb-1">{msg.speaker}</div>
                    <div>{msg.message}</div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default AIChatInterface;