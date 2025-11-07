'use client'

import { useEffect, useRef } from 'react'
import Message from './Message';

/**
 * MessageStream component that displays a list of messages
 * @param {Object} props
 * @param {Array} props.messages - Array of message objects with { role, content }
 */
const MessageStream = ({ messages = [] }) => {
    const messagesEndRef = useRef(null);

    // Auto-scroll to bottom when new messages are added
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    if (messages.length === 0) {
        return (
            <div className="flex-1 flex items-center justify-center px-4">
                <p className="text-4xl font-semibold">
                    Welcome to <span className="italic">Capybara AI</span>
                </p>
            </div>
        );
    }

    return (
        <div className="flex-1 overflow-y-auto px-4 py-6 flex justify-center h-full">
            <div className="flex flex-col max-w-xl w-full gap-2">
                {messages.map((message, index) => (
                    <Message
                        key={index}
                        role={message.role}
                        content={message.content}
                    />
                ))}
                <div ref={messagesEndRef} />
            </div>
        </div>
    );
};

export default MessageStream;