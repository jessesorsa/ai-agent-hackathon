'use client'

import { useState } from 'react'
import InputBox from "@/components/components/InputBox";
import MessageStream from "@/components/components/MessageStream";
//import GenerativeUi from '@/components/components/GenerativeUi';

export default function Dashboard() {
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [ui, setUi] = useState({});

    const handleMessageSent = (message) => {
        setMessages(prev => [...prev, message]);
    };

    const handleResponseReceived = (message) => {
        setMessages(prev => [...prev, message]);
    };

    return (
        <div className="flex flex-col min-h-screen bg-background">
            <div className="flex-1 overflow-hidden flex pb-32">
                <MessageStream messages={messages} isLoading={isLoading} />
                {/*<GenerativeUi ui={ui} />*/}
            </div>
            <InputBox
                onMessageSent={handleMessageSent}
                onResponseReceived={handleResponseReceived}
                setUi={setUi}
                setIsLoading={setIsLoading}
            />
        </div>
    );
}

