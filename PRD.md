# AI Sales Assistant — Product Requirements Document (PRD)

Last updated: 2025-11-07

## One-line summary

Build an AI-powered sales assistant that automates repetitive sales workflows through specialized agents that handle CRM management, email drafting, company research, and meeting documentation.

## Context & motivation

This is a hackathon project. The repo contains a Next.js frontend (`/frontend`) and a Python backend (`/backend/main.py`). The goal is to ship a working AI sales assistant that orchestrates multiple specialized agents to streamline the sales process—from lead discovery to meeting follow-ups.

Why this matters:
- Founders and sales teams waste hours on manual CRM updates, research, and email drafting
- Demonstrates real-world multi-agent orchestration solving actual business pain
- Shows practical LLM integration with external tools (CRM, Gmail, web search, Notion)
- Delivers a compelling demo showing end-to-end automation of a sales workflow

## Goals (success criteria)

- MVP should demonstrate lead discovery → CRM creation → email drafting in one flow
- Demo should show agents working together (web search → CRM → Gmail)
- UI should clearly show agent reasoning and handoffs between agents
- For hackathon judging: produce a clear demo showing time savings vs manual process

Success metrics (measurable):
- End-to-end lead qualification flow working: PASS/FAIL
- Time to research company + add to CRM + draft email < 2 minutes
- At least 3 agents working in orchestration (Web Search, CRM, Gmail)
- ICP fit assessment accuracy > 80%

## Target users & personas

Primary user: Founders doing founder-led sales
- Limited time, needs to qualify leads quickly
- Manually juggling CRM, email, research tools
- Wants to focus on selling, not admin work

Secondary user: Early-stage sales teams / SDRs
- High volume of lead qualification needed
- Spending too much time on manual data entry
- Need to personalize outreach at scale

Personas:
- Alex, Startup Founder: Needs to qualify 20 leads/week, currently takes 30min each
- Sarah, SDR: Needs to send 50 personalized emails/day, currently spends 3 hours on research and drafting

## Key user stories

1. As a founder, I can give a company name and get an ICP fit assessment with key data points
2. As a founder, I can automatically add qualified leads to my CRM with enriched data
3. As an SDR, I can get a personalized email draft that uses context from CRM and recent company news
4. As a sales rep, I can ask questions about my deals and get instant answers from CRM
5. As a founder, I can get a pre-meeting brief that pulls all relevant context automatically

## MVP feature set (scope for hackathon)

### Core Agents (MVP):

**Web Search Agent**
- Search company information (size, industry, funding, tech stack)
- Find decision-maker names and roles
- Assess ICP fit based on criteria from Notion
- Extract recent company news

**CRM Agent**
- Create company records
- Create contact records
- Update existing records
- Search for records
- Add notes to records

**Gmail Agent**
- Draft personalized outreach emails
- Use CRM context (company info, deal stage)
- Adapt tone based on sales stage

**Notion Agent**
- Fetch ICP criteria document
- Retrieve product information

**Orchestrator**
- Coordinate agent handoffs
- Maintain context between agents
- Handle error recovery and retries

### UI Features (MVP):
- Natural language input for tasks
- Agent activity visualizer (which agent is working)
- Step-by-step execution display with agent reasoning
- Structured output for CRM data (cards/tables)
- Confirmation prompts before writing to CRM
- Export/copy draft emails

### Stretch / nice-to-have (if time permits):
- Meeting transcription agent
- Bulk lead processing (CSV upload)
- Email send integration (vs just drafting)
- Deal pipeline visualization

## User flows

### Flow 1: Lead Discovery & Qualification (Primary Demo Flow)

**User Intent**: "Research Stripe and tell me if they fit our ICP, then add them to CRM"

1. User opens app and enters task in natural language
2. Frontend sends to backend: `POST /api/task { intent: "Research Stripe..." }`
3. **Orchestrator** creates execution plan:
   - Step 1: Web Search Agent researches Stripe
   - Step 2: Notion Agent fetches ICP criteria
   - Step 3: Web Search Agent scores ICP fit
   - Step 4: CRM Agent creates company record
4. UI displays plan with agent assignments
5. User confirms plan execution
6. **Web Search Agent** executes:
   - Searches for Stripe company info
   - UI shows: "Searching for Stripe information..."
   - Returns: company size (8000+ employees), industry (fintech), funding ($2.2B)
7. **Notion Agent** executes:
   - Fetches ICP criteria
   - UI shows: "Retrieving ICP criteria from Notion..."
   - Returns: target company size (50-2000), industry (B2B SaaS, fintech)
8. **Web Search Agent** scores:
   - UI shows: "Assessing ICP fit..."
   - Returns: "Poor fit - company too large (8000 vs target 50-2000)"
   - ICP Score: 3/10
9. System asks: "Company doesn't match ICP. Add to CRM anyway?"
10. User can:
    - Approve → CRM Agent creates record
    - Skip → End flow
    - Modify ICP criteria → Rescore

### Flow 2: Pre-Meeting Preparation

**User Intent**: "Prepare me for my meeting with Acme Corp tomorrow"

1. User enters task
2. **Orchestrator** creates plan:
   - Step 1: CRM Agent retrieves Acme Corp record
   - Step 2: Web Search Agent finds recent news
   - Step 3: Orchestrator compiles meeting brief
3. **CRM Agent** executes:
   - Searches CRM for "Acme Corp"
   - Returns: company data, deal status, contact info, previous notes
4. **Web Search Agent** executes:
   - Searches for recent Acme Corp news
   - Returns: "Acme Corp raised Series B $50M last week"
5. **Orchestrator** compiles:
   - Meeting brief card displayed with sections:
     - Company background
     - Current deal status
     - Key contacts
     - Recent news/talking points
     - Suggested next steps
6. User can copy brief or export to notes

### Flow 3: Email Drafting

**User Intent**: "Draft a follow-up email to john@acme.com"

1. User enters task
2. **Orchestrator** creates plan:
   - Step 1: CRM Agent looks up contact
   - Step 2: CRM Agent gets recent interactions
   - Step 3: Gmail Agent drafts email
3. **CRM Agent** executes:
   - Searches for john@acme.com
   - Returns: John Smith, CTO at Acme Corp, last contacted 2 weeks ago
   - Retrieves: last meeting notes, deal stage (Demo Scheduled)
4. **Gmail Agent** executes:
   - Uses context to draft personalized email
   - UI shows: "Drafting email with context..."
   - Returns: email draft with personalized content
5. UI displays draft in editable text box
6. User can:
   - Copy to clipboard
   - Edit and regenerate
   - (Stretch) Send directly via Gmail API

### Flow 4: Quick CRM Query

**User Intent**: "What's the status of the Acme Corp deal?"

1. User enters question
2. **CRM Agent** executes:
   - Searches for Acme Corp deal
   - Returns: Deal stage, amount, last activity, next steps
3. UI displays structured card with deal info
4. Fast response (< 5 seconds)

### Edge Flows:
- **Rate limit**: Agent shows error, auto-retries with exponential backoff
- **Not found in CRM**: Agent offers to search web instead
- **Ambiguous query**: Agent asks clarifying question
- **Write action confirmation**: Always prompt before CRM writes

## UI Screens (textual wireframes)

### Main Screen
```
┌─────────────────────────────────────────────────────┐
│ AI Sales Assistant                          [⚙️]    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  What would you like to do?                         │
│  ┌────────────────────────────────────────────┐    │
│  │ Research Acme Corp and assess ICP fit...   │    │
│  │                                      [Send]│    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  Quick actions:                                      │
│  [🔍 Research Company] [✉️ Draft Email]             │
│  [📊 Get Deal Status] [📅 Meeting Prep]             │
│                                                      │
├─────────────────────────────────────────────────────┤
│  Agent Activity                                      │
│  ● Web Search Agent - Idle                          │
│  ● CRM Agent - Idle                                  │
│  ● Gmail Agent - Idle                                │
│  ● Notion Agent - Idle                               │
└─────────────────────────────────────────────────────┘
```

### Execution Screen (during task)
```
┌─────────────────────────────────────────────────────┐
│ Task: Research Stripe and assess ICP fit            │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Plan (4 steps)                          [⏸️ Pause]  │
│                                                      │
│ ✅ 1. Web Search - Research Stripe                  │
│    Found: 8000+ employees, Fintech, $2.2B funding   │
│                                                      │
│ ✅ 2. Notion - Fetch ICP criteria                   │
│    Target: 50-2000 employees, B2B SaaS              │
│                                                      │
│ 🔄 3. Web Search - Assess ICP fit                   │
│    Analyzing fit...                                  │
│                                                      │
│ ⏳ 4. CRM - Create company record                   │
│    Waiting...                                        │
│                                                      │
├─────────────────────────────────────────────────────┤
│ Agent Activity                                       │
│ 🔄 Web Search Agent - Assessing ICP fit            │
└─────────────────────────────────────────────────────┘
```

### Results Screen
```
┌─────────────────────────────────────────────────────┐
│ Results: Stripe ICP Assessment               [✕]    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ICP Fit Score: 3/10 ❌ Poor Fit                    │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │ Stripe                                       │   │
│  │ Industry: Fintech, Payments                  │   │
│  │ Size: 8,000+ employees                       │   │
│  │ Funding: $2.2B total raised                  │   │
│  │ HQ: San Francisco, CA                        │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
│  Why poor fit:                                       │
│  ❌ Company size (8000) exceeds target (50-2000)   │
│  ✅ Industry (fintech) matches                      │
│  ❌ Likely has enterprise sales team already        │
│                                                      │
│  [Skip] [Add to CRM Anyway] [Adjust ICP Criteria]   │
└─────────────────────────────────────────────────────┘
```

### Email Draft Screen
```
┌─────────────────────────────────────────────────────┐
│ Draft Email: Follow-up to John Smith         [✕]    │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Context used:                                        │
│ • Contact: John Smith (CTO, Acme Corp)              │
│ • Last contact: 2 weeks ago                          │
│ • Deal stage: Demo Scheduled                         │
│ • Last meeting: Discussed integration requirements   │
│                                                      │
│ ┌─────────────────────────────────────────────┐   │
│ │ To: john@acme.com                            │   │
│ │ Subject: Following up on integration demo    │   │
│ │                                               │   │
│ │ Hi John,                                      │   │
│ │                                               │   │
│ │ Hope you're doing well! Following up on our  │   │
│ │ conversation two weeks ago about integrating │   │
│ │ our solution with your existing stack.       │   │
│ │                                               │   │
│ │ I wanted to check if you had a chance to...  │   │
│ │                                               │   │
│ └─────────────────────────────────────────────┘   │
│                                                      │
│ [📋 Copy] [🔄 Regenerate] [✏️ Edit] [📧 Send]      │
└─────────────────────────────────────────────────────┘
```

## API Contract

### Core Endpoints

**POST /api/task**
```json
Request:
{
  "intent": "Research Stripe and assess ICP fit",
  "sessionId": "optional-session-id"
}

Response:
{
  "taskId": "task-123",
  "plan": {
    "steps": [
      {
        "id": "step-1",
        "agent": "web_search",
        "action": "research_company",
        "params": { "company": "Stripe" },
        "status": "pending"
      },
      ...
    ]
  }
}
```

**GET /api/task/{taskId}/status**
```json
Response:
{
  "taskId": "task-123",
  "status": "running",
  "currentStep": 2,
  "steps": [...with updated statuses],
  "results": {...}
}
```

**WebSocket /ws/task/{taskId}**
```json
Real-time updates:
{
  "type": "step_update",
  "stepId": "step-2",
  "status": "running",
  "message": "Fetching ICP criteria from Notion...",
  "agent": "notion"
}
```

### Agent-Specific Endpoints

**POST /api/agents/web_search/research**
```json
Request:
{
  "company": "Stripe",
  "aspects": ["size", "industry", "funding", "contacts"]
}

Response:
{
  "company": "Stripe",
  "size": "8000+",
  "industry": "Fintech",
  "funding": "$2.2B",
  "sources": [...]
}
```

**POST /api/agents/crm/create_company**
```json
Request:
{
  "name": "Stripe",
  "size": "8000+",
  "industry": "Fintech",
  "confirmed": true
}

Response:
{
  "id": "company-456",
  "url": "notion.so/company-456"
}
```

**POST /api/agents/gmail/draft**
```json
Request:
{
  "to": "john@acme.com",
  "context": {
    "contactId": "contact-123",
    "dealStage": "demo_scheduled"
  }
}

Response:
{
  "subject": "Following up on integration demo",
  "body": "Hi John,...",
  "contextUsed": [...]
}
```

Auth: Session-based for MVP (no OAuth needed for demo)

## Acceptance Criteria (Definition of Done)

### Must-Have for MVP Demo:

1. **Lead Discovery Flow Works End-to-End**
   - User can input "Research [Company] and assess ICP fit"
   - Web Search Agent researches company info
   - Notion Agent fetches ICP criteria
   - System provides ICP fit score with reasoning
   - User can confirm to add to CRM
   - CRM Agent creates company record

2. **Agent Orchestration Visible**
   - UI shows which agent is currently executing
   - Plan displays before execution with agent assignments
   - Step-by-step status updates (pending → running → complete/failed)
   - Agent reasoning displayed for each step

3. **Email Drafting Works**
   - User can request email draft for a contact
   - CRM Agent retrieves contact context
   - Gmail Agent generates personalized draft
   - User can copy draft

4. **Real Integrations (at least 2 of 3)**
   - Web search using real API (SerpAPI/Bing/Perplexity)
   - Notion API for ICP criteria OR mock with realistic data
   - Notion CRM OR simple database for company records

5. **Demo Completes in < 2 Minutes**
   - Full lead discovery flow runs in under 2 minutes
   - No manual delays or waiting

### Success Criteria:

- ✅ End-to-end demo works without errors
- ✅ UI is polished enough for demo (not production, but clean)
- ✅ Agent handoffs are smooth and logical
- ✅ At least 3 different agents working together
- ✅ Can demonstrate on real company examples (Stripe, Notion, etc.)

## Tech Stack

### Frontend
- **Framework**: Next.js 14+ (existing `/frontend`)
- **UI Components**: Tailwind CSS + shadcn/ui for clean, modern UI
- **Real-time**: WebSocket client for live agent updates
- **State Management**: React Context or Zustand for agent status

### Backend
- **Framework**: FastAPI (Python, existing `/backend/main.py`)
- **LLM Orchestration**: LangGraph or custom orchestrator
- **LLM**: OpenAI GPT-4 (function calling for agent routing)
- **WebSockets**: FastAPI WebSocket for real-time updates

### Agent Integrations
- **Web Search**: Perplexity API or SerpAPI (easiest for hackathon)
- **CRM**: Notion API (database for companies/contacts) OR simple SQLite
- **Email**: Mock Gmail Agent (no real sending needed for MVP)
- **Notion**: Notion API for fetching ICP documents

### Storage
- **MVP**: In-memory with Python dictionaries
- **If needed**: SQLite for persistence
- **Not needed**: Redis, PostgreSQL (overkill for hackathon)

### Development
- **Local Development**: `npm run dev` for frontend, `uvicorn` for backend
- **No Docker**: Run directly for faster iteration
- **Environment**: `.env` file for API keys

### Key Libraries
```python
# Backend
fastapi
langchain / langgraph
openai
notion-client
requests (for web search APIs)
websockets
```

```typescript
// Frontend
next
tailwindcss
socket.io-client or native WebSocket
```

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| API rate limits during demo | High | Cache responses, use mock data as fallback |
| LLM returns inconsistent plan | Medium | Structured output with JSON schema, retry logic |
| Web search returns poor data | Medium | Hardcode fallback data for demo companies (Stripe, Notion) |
| Agent handoff failures | High | Extensive testing of orchestrator, clear error messages |
| Demo too slow (>2 min) | High | Optimize API calls, parallel execution where possible |
| Notion API setup complexity | Medium | Use SQLite as simpler alternative for CRM |
| Real-time updates lag | Low | Polling fallback if WebSocket fails |

## Testing Strategy

### Manual Testing (Priority)
1. **End-to-end demo script** (must work 100%):
   - "Research Stripe and assess ICP fit, then add to CRM"
   - "Draft follow-up email to john@stripe.com"
   - "What's the status of the Stripe deal?"

2. **Edge cases to test**:
   - Company not found by web search
   - Bad ICP fit score
   - Contact not in CRM
   - API timeout/failure

3. **Performance testing**:
   - Time each flow with stopwatch
   - Optimize if > 2 minutes

### Automated Testing (Nice-to-have)
- Unit tests for agent tool functions
- Schema validation for API responses
- Not critical for hackathon demo

### Pre-Demo Checklist
- [ ] Run full demo 3 times successfully
- [ ] Record backup demo video
- [ ] Test on fresh browser (clear cache)
- [ ] API keys loaded and working
- [ ] Hardcoded demo data ready as fallback

## Implementation Timeline (Hackathon - 48 hours)

### Phase 1: Foundation (Hours 0-8)
**Backend**
- [ ] Set up FastAPI with WebSocket support
- [ ] Create basic orchestrator (route intent → agents)
- [ ] Implement Web Search Agent (Perplexity/SerpAPI)
- [ ] Implement mock CRM Agent (in-memory)
- [ ] Create task execution engine

**Frontend**
- [ ] Set up main UI with input box
- [ ] Create agent status display component
- [ ] Build step-by-step execution viewer
- [ ] Add WebSocket connection

**Milestone**: Can submit task and see agents execute

### Phase 2: Core Flows (Hours 8-24)
**Backend**
- [ ] Build ICP assessment logic
- [ ] Add Notion Agent (fetch ICP criteria)
- [ ] Implement Gmail Agent (email drafting)
- [ ] Add CRM search and create functions
- [ ] Refine orchestrator for multi-agent flows

**Frontend**
- [ ] Build ICP assessment results card
- [ ] Create email draft viewer with copy button
- [ ] Add confirmation dialogs for CRM writes
- [ ] Polish UI styling

**Milestone**: Lead discovery flow works end-to-end

### Phase 3: Polish & Demo Prep (Hours 24-40)
- [ ] Add error handling and retries
- [ ] Implement hardcoded fallback data
- [ ] Add loading states and animations
- [ ] Write demo script
- [ ] Test all flows 3x
- [ ] Optimize for speed (<2 min)

**Milestone**: Demo-ready system

### Phase 4: Final Polish (Hours 40-48)
- [ ] Record demo video
- [ ] Create README with setup instructions
- [ ] Prepare presentation deck
- [ ] Practice demo 5x
- [ ] Buffer for last-minute bugs

**Milestone**: Submission ready

## Deliverables

### Required for Submission
1. **Working Web App**
   - Frontend accessible at `localhost:3000`
   - Backend running at `localhost:8000`
   - Lead discovery flow functional

2. **Demo Video (3-5 minutes)**
   - Show lead discovery flow
   - Show email drafting
   - Highlight agent orchestration
   - Explain time savings

3. **Documentation**
   - README with setup instructions
   - Demo script for judges
   - Architecture diagram (simple)

4. **Presentation (optional but recommended)**
   - Problem statement
   - Solution overview
   - Live demo
   - Technical highlights

## Out of Scope (Explicitly NOT Building)

- ❌ Production authentication/authorization
- ❌ Real Gmail sending (just drafting)
- ❌ Meeting transcription (stretch feature)
- ❌ Advanced CRM features (pipelines, forecasting)
- ❌ Mobile responsive design
- ❌ Comprehensive error handling
- ❌ Data persistence beyond in-memory
- ❌ User accounts/multi-tenancy

## Success Definition

**Minimum Viable Demo:**
- User inputs "Research Stripe and assess ICP fit"
- Web Search Agent finds Stripe data
- Notion Agent gets ICP criteria
- System scores fit (shows "poor fit - too large")
- User can confirm to add to CRM anyway
- CRM Agent creates record
- Total time: < 2 minutes

**Stretch Goals:**
- Email drafting works
- Pre-meeting brief works
- 3+ companies pre-loaded in CRM for demos
- Beautiful UI that impresses judges

## Next Immediate Steps

1. Set up backend FastAPI structure
2. Create orchestrator skeleton
3. Build Web Search Agent
4. Create frontend task input page
5. Connect WebSocket for real-time updates
