'use client'

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import {
    Card,
    CardContent,
} from "@/components/ui/card"
//import { test, sendInput } from '@/http/http'

const InputBox = () => {
    const [input, setInput] = useState("");

    /*
    const dispatch = useDispatch();
    const messages = useSelector((state) => state.chat.messages);
    const last_5_messages = useSelector((state) => selectLastMessages(state, 0));

    const sendMessage = async () => {
        dispatch(addMessage({
            role: 'user',
            content: input,
        }))

        const messageStream = [...last_5_messages, input];
        setInput("");
        const data = await sendInput(messageStream);

        if (data && data.role && data.content) {
            dispatch(addMessage(data));
            return;
        }

        const outputs = [];

        for (const [key, value] of Object.entries(data)) {
            if (key === 'answer') {
                outputs.push({
                    role: 'assistant',
                    content: value
                });
            } else if (value.role && value.content) {
                outputs.push({
                    role: value.role,
                    content: value.content
                });
            }
        }

        for (const message of outputs) {
            dispatch(addMessage(message));
        }
        */

    const sendMessage = () => {
        // TODO: Implement sendMessage functionality
    };

    return (
        <div className="fixed bottom-4 left-0 right-0 z-10 flex justify-center px-">
            <Card className="flex p-2 w-full max-w-2xl mx-auto bg-neutral-600">
                <CardContent className="flex flex-col p-0 gap-2">
                    <div className="flex flex-row">
                        <Textarea
                            className="text-md w-full h-20 shadow-none resize-none outline-none ring-0 border-0 focus:ring-0 focus:border-0 focus-visible:ring-0 focus-visible:border-0"
                            placeholder="Chat with your database"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                        />
                        <Button
                            className="rounded-full"
                            onClick={sendMessage}>
                            Send
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

export default InputBox;