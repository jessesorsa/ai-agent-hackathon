'use client'

import { Card, CardContent } from "@/components/ui/card";
import ReactMarkdown from "react-markdown";
import 'github-markdown-css/github-markdown.css'

/**
 * Message component that displays a single message
 * @param {Object} props
 * @param {string} props.role - 'user' or 'agent'
 * @param {string} props.content - The message content
 * @param {string} props.className - Additional CSS classes
 */
const Message = ({ role, content, className }) => {
    if (role === 'user') {
        return (
            <div className="flex justify-start">
                <Card
                    className="p-3 w-fit shadow-none border-none bg-neutral-100">
                    <CardContent
                        className="p-0">
                        {content}
                    </CardContent>
                </Card >
            </div>
        );
    }

    // Agent message
    return (
        <div className="flex justify-start">
            <Card
                className="p-3 max-w-full border-none shadow-none bg-white">
                <CardContent
                    className="p-0">
                    <article className="markdown-body break-words overflow-x-auto max-w-full">
                        <ReactMarkdown>
                            {content}
                        </ReactMarkdown>
                    </article>
                </CardContent>
            </Card >
        </div>
    );
};

export default Message;

