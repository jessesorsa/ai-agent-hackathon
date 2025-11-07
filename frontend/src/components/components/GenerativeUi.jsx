'use client'
import { C1Component } from "@thesysai/genui-sdk";
import "@crayonai/react-ui/styles/index.css";

/**
 * GenerativeUi component that displays generative UI from agent response
 * @param {Object} props
 * @param {string} props.message - The agent message content to display
 */
const GenerativeUi = ({ message = '' }) => {
    // Don't render if no message
    if (!message) {
        return null;
    }

    return <C1Component c1Response={message} />;
};

export default GenerativeUi;