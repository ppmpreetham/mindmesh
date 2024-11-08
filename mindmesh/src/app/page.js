"use client"
import { useEffect } from 'react';
import useAIConversation from './/hooks/useAIConversation'; // Import the custom hook

const Home = () => {
    const { conversation, startConversation, loading } = useAIConversation();

    useEffect(() => {
        // Start the conversation when the page loads
        startConversation("Hey, how are you?");
    }, []);

    return (
        <div>
            <h1>AI Interaction</h1>

            {loading ? (
                <p>Loading...</p>
            ) : (
                <div>
                    {conversation.map((msg, index) => (
                        <p key={index}>{msg}</p>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Home;