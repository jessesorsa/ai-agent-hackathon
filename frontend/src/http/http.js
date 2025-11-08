/**
 * HTTP client for making API requests to the backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Sends a POST request to the backend with the user's input
 * @param {string|Array} messageData - The message or array of messages to send
 * @returns {Promise<Object>} The response from the backend
 */
export const sendInput = async (messageData) => {
    try {
        console.log(messageData);
        const response = await fetch(`${API_BASE_URL}/orchestrator_agent`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: messageData,
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Transform backend response to match MessageStream format
        // Backend returns: {"message": "..."}
        // We need: {"content": "...", "role": "agent"}
        return {
            content: data.message || data.content || "",
            role: 'agent'
        };
    } catch (error) {
        console.error('Error sending message:', error);
        throw error;
    }
};

/**
 * Test function (placeholder)
 * @returns {Promise<Object>} Test response that will be routed to agent message
 */
export const test = async () => {
    return {
        content: `# Welcome to the CRM Assistant

This is a **markdown-enabled** test message from the agent. The test endpoint is working correctly!

## Features

Here are some key features:

- **Markdown Support**: Agent messages can now display formatted text
- **Code Blocks**: You can include code examples
- **Lists**: Both ordered and unordered lists work
- **Links**: [Click here](https://example.com) for more info

### Code Example

\`\`\`javascript
const example = () => {
    console.log("Hello, World!");
    return "Markdown is working!";
};
\`\`\`

### Additional Information

> This is a blockquote example. It's great for highlighting important information.

You can also use **bold text**, *italic text*, and \`inline code\` within your messages.

#### Summary

The markdown rendering is now fully functional and ready to display rich content from the backend!`,
        role: 'agent'
    };
};

