'use client'

import { useState } from 'react'
import { ArrowUp } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import {
    Card,
    CardContent,
} from "@/components/ui/card"
import { sendInput, test } from '@/http/http'

/**
 * InputBox component for sending messages
 * @param {Object} props
 * @param {Function} props.onMessageSent - Callback function called when a message is sent
 * @param {Function} props.onResponseReceived - Callback function called when a response is received
 * @param {Array} props.messages - Array of previous messages for context
 */
const InputBox = ({ onMessageSent, onResponseReceived, setUi, setIsLoading, messages = [] }) => {
    const [input, setInput] = useState("");

    const sendMessage = async () => {
        if (!input.trim()) return;

        const currentInput = input;
        setInput("");
        setIsLoading(true);

        // Add user message to stream
        if (onMessageSent) {
            onMessageSent({
                role: 'user',
                content: currentInput
            });
        }

        try {
            // Get last 3 messages for context
            const last3Messages = messages.slice(-3);

            // Send current input with context messages
            const response = await sendInput(currentInput, last3Messages);
            console.log('Response from backend:', response);

            // Handle the response
            if (onResponseReceived) {
                // Try to parse content as JSON if it's a string
                let parsedResponse = response;

                if (response.content && typeof response.content === 'string') {
                    try {
                        // Try to parse the content as JSON
                        const parsedContent = JSON.parse(response.content);
                        // If parsed content has a role, use it
                        if (parsedContent.role) {
                            parsedResponse = parsedContent;
                        }
                    } catch (e) {
                        // Not valid JSON, continue with original response
                    }
                }

                // If response already has a role (either from parsing or original), use it directly
                if (parsedResponse.role) {
                    onResponseReceived(parsedResponse);
                }
                // Otherwise, default to agent role with content/answer
                else if (response.content || response.answer) {
                    onResponseReceived({
                        role: 'agent',
                        content: response.content || response.answer
                    });
                }
            }

        } catch (error) {
            console.error('Failed to send message:', error);
            // Optionally add error message to stream
            if (onResponseReceived) {
                onResponseReceived({
                    role: 'agent',
                    content: 'Sorry, there was an error processing your request.'
                });
            }
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className="fixed bottom-4 left-0 right-0 z-10 flex justify-center px-4">
            <Card className="flex p-2 w-2xl rounded-3xl bg-neutral-100/70 backdrop-blur-sm shadow-xl">
                <CardContent className="flex flex-col p-0 gap-2">
                    <div className="flex flex-row">
                        <Textarea
                            className="w-full text-xl mt-1 shadow-none bg-transparent resize-none outline-none ring-0 border-0 focus:ring-0 focus:border-0 focus-visible:ring-0 focus-visible:border-0"
                            placeholder="Use your sales stack..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                        />
                        <Button
                            size="icon"
                            className="rounded-full bg-black"
                            onClick={sendMessage}>
                            <ArrowUp className="w-6 h-6" />
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

export default InputBox;