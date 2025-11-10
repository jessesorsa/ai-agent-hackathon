# Capybara AI

Capybara AI is a unified interface for managing your CRM and sales applications. Interact with HubSpot, Gmail, Slack, Google Calendar, and Notion through natural language commands in a single, intuitive chat interface.

## Overview

Capybara AI simplifies your sales workflow by providing a conversational AI assistant that can:
- Search and manage CRM records (companies, deals, contacts)
- Draft and send emails
- Manage calendar events
- Send Slack messages
- Search the web and manage Notion pages
- Display information in generative components

All through a simple chat interface powered by AI agents.

## Features

### 🤖 Intelligent Agent Orchestration
- **Orchestrator Agent**: Routes your requests to the appropriate specialized agent
- **HubSpot Agent**: Manage CRM operations (companies, deals, contacts)
- **Gmail Agent**: Handle email drafting and sending
- **Slack Agent**: Send messages and manage Slack conversations
- **Calendar Agent**: Create and manage calendar events
- **Data Agent**: Web search and Notion page management

### 🎨 Rich UI Components
- **Company Cards**: Display company information with ICP fit scores, industry details, and more
- **Event Cards**: Show calendar events and meetings
- **Data Tables**: Display multiple records in organized tables
- **Markdown Support**: Rich text formatting for agent responses

### 💬 Conversational Interface
- Natural language commands
- Conversation context awareness (last 3 messages)
- Real-time responses
- Dark mode support

## Architecture

### Frontend
- **Framework**: Next.js 16 with React 19
- **Styling**: Tailwind CSS with shadcn/ui components
- **State Management**: React hooks
- **HTTP Client**: Fetch API

### Backend
- **Framework**: FastAPI
- **AI Agents**: OpenAI Agents SDK with Composio integration
- **LLM**: GPT-4.1-mini
- **Integrations**: 
  - HubSpot (via Composio)
  - Gmail (via Composio)
  - Slack (via Composio)
  - Google Calendar (via Composio)
  - Notion (via Composio)
  - Perplexity AI (web search)

## Project Structure

```
AI-agent-hackathon/
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/
│   │   │   └── dashboard/   # Main dashboard page
│   │   ├── components/
│   │   │   ├── components/  # Message, InputBox, MessageStream
│   │   │   └── ui/          # shadcn/ui components
│   │   └── http/            # API client
│   └── package.json
│
└── backend/                # FastAPI backend
    ├── ai_agents/           # Agent implementations
    │   ├── orchestrator_agent.py
    │   ├── hubspot_agent.py
    │   ├── gmail_agent.py
    │   ├── slack_agent.py
    │   ├── calendar_agent.py
    │   └── data_agent.py
    ├── main.py              # FastAPI application
    └── setup.md             # Setup instructions
```

## Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.12+
- API Keys:
  - OpenAI API key
  - Composio API key
  - Thesys API key (for UI generation)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python3 -m venv ai-hackathon
source ai-hackathon/bin/activate  # On Windows: ai-hackathon\Scripts\activate
```

3. Install dependencies:
```bash
# Install directly with pip
pip install fastapi uvicorn[standard] python-dotenv openai composio composio-openai-agents openai-agents

# Or install from requirements.txt
pip install -r requirements.txt
```

4. Create `.env` from the example:
```bash
cp .env.example .env
```
Then open `.env` and fill in your API keys and IDs (e.g. OPENAI_API_KEY, COMPOSIO_API_KEY, THESYS_API_KEY, GMAIL_USER_ID).

5. Run the server:
```bash
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. Open the dashboard at `http://localhost:3000/dashboard`
2. Type your request in natural language, for example:
   - "Search for companies named Acme"
   - "Create a calendar event for tomorrow at 2pm"
   - "Draft an email to john@example.com about the meeting"
   - "Show me all deals over $50k"
3. The orchestrator agent will route your request to the appropriate agent
4. Results are displayed as interactive components (cards, tables) or formatted text

## API Endpoints

- `POST /orchestrator_agent` - Main endpoint for all requests
- `POST /hubspot_agent` - Direct HubSpot operations
- `POST /gmail_agent` - Direct Gmail operations
- `POST /calendar_agent` - Direct calendar operations
- `POST /ui_agent` - UI generation endpoint

## Tech Stack

### Frontend
- Next.js 16
- React 19
- Tailwind CSS
- shadcn/ui
- Lucide React (icons)
- react-markdown

### Backend
- FastAPI
- OpenAI Agents SDK
- Composio SDK
- Python 3.12
