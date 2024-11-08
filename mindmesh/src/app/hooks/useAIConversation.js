import { useState } from 'react';
import ollama from 'ollama'; // Import ollama SDK

const useAIConversation = () => {
    const [conversation, setConversation] = useState([]);
    const [loading, setLoading] = useState(false);

    const startConversation = async (initialMessage) => {
        setLoading(true);
        const conversationMessages = [initialMessage];
        
        // Start the conversation with the first message
        try {
            for (let i = 0; i < 5; i++) {  // Simulate back-and-forth AI interaction
                const aiResponse = await ollama.chat({
                    model: 'openhermes',  // Choose the model you want to interact with
                    messages: [
                        { role: 'user', content: conversationMessages[i] },
                    ],
                });

                const aiMessage = aiResponse.message.content;
                conversationMessages.push(aiMessage);  // Add AI response to conversation

                if (aiMessage.toLowerCase().includes('bye')) {
                    break;  // End the conversation if AI says "bye"
                }
            }

            setConversation(conversationMessages);
        } catch (error) {
            console.error('Error interacting with Ollama:', error);
            setConversation(['Sorry, something went wrong.']);
        } finally {
            setLoading(false);
        }
    };

    return { conversation, startConversation, loading };
};

export default useAIConversation;