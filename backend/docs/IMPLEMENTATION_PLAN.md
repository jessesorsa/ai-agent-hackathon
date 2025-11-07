# AI Sales Assistant - Backend Implementation Plan

## Overview
This document provides a phase-by-phase implementation plan for the AI Sales Assistant backend using **LangGraph** for agent orchestration and **LangChain** for LLM integration. Each phase is designed to be executed sequentially by an AI model or developer, with clear acceptance criteria and deliverables.

---

## Phase 1: Core Infrastructure Setup

### Goal
Set up the foundational FastAPI backend with basic routing, WebSocket support, and project structure.

### Tasks
1. **Project Structure Setup**
   - Create directory structure:
     ```
     backend/
     ├── main.py                 # FastAPI app entry point
     ├── api/
     │   ├── __init__.py
     │   ├── routes/
     │   │   ├── __init__.py
     │   │   ├── task.py        # Task endpoints
     │   │   └── agents.py      # Agent-specific endpoints
     │   └── websocket.py       # WebSocket handler
     ├── core/
     │   ├── __init__.py
     │   ├── config.py          # Configuration and env vars
     │   └── schemas.py         # Pydantic models
     ├── agents/
     │   ├── __init__.py
     │   ├── base.py            # Base agent class
     │   ├── web_search.py      # Web Search Agent
     │   ├── hubspot.py         # HubSpot CRM Agent
     │   ├── gmail.py           # Gmail Agent
     │   └── notion.py          # Notion Agent
     ├── graph/
     │   ├── __init__.py
     │   ├── state.py           # LangGraph state definitions
     │   ├── nodes.py           # LangGraph node implementations
     │   ├── workflow.py        # LangGraph workflow builder
     │   └── tools.py           # LangChain tools
     └── utils/
         ├── __init__.py
         └── storage.py         # In-memory storage
     ```

2. **Dependencies Installation**
   - Create `requirements.txt` with:
     ```
     fastapi==0.104.1
     uvicorn[standard]==0.24.0
     websockets==12.0
     pydantic==2.5.0
     python-dotenv==1.0.0
     openai==1.3.0
     httpx==0.25.0
     langchain==0.1.0
     langgraph==0.0.20
     langchain-openai==0.0.2
     langchain-community==0.0.10
     composio-langchain==0.3.0
     ```
   - Create `.env.example` file with placeholder API keys

3. **FastAPI App Initialization**
   - Set up main.py with:
     - FastAPI app instance
     - CORS middleware
     - Health check endpoint: `GET /health`
     - Root endpoint: `GET /`
   - Add basic error handlers

4. **Configuration Management**
   - Implement `core/config.py`:
     - Load environment variables
     - API key validation
     - Configuration class with settings
     - Initialize LangChain LLM instances

5. **Pydantic Schemas**
   - Create `core/schemas.py` with:
     - `TaskRequest`: User intent input
     - `TaskResponse`: Task creation response
     - `StepSchema`: Individual step in execution plan
     - `PlanSchema`: Complete execution plan
     - `TaskStatus`: Status tracking model
     - `WebSocketMessage`: Real-time update format
     - `AgentState`: LangGraph state schema

### Acceptance Criteria
- [ ] FastAPI server starts successfully with `uvicorn backend.main:app --reload`
- [ ] `GET /health` returns `{"status": "healthy"}`
- [ ] Project structure matches specification
- [ ] Environment variables load correctly from `.env`
- [ ] All Pydantic schemas validate correctly with test data
- [ ] LangChain LLM initializes successfully

### Deliverables
- Working FastAPI server
- Complete project structure
- Configuration management
- Core data schemas
- LangChain setup

---

## Phase 2: In-Memory Storage & Task Management

### Goal
Implement in-memory storage for tasks and create basic task management endpoints.

### Tasks
1. **Storage Layer**
   - Implement `utils/storage.py`:
     - `TaskStore` class with in-memory dict
     - Methods: `create_task()`, `get_task()`, `update_task()`, `list_tasks()`
     - Thread-safe operations using locks
     - Task ID generation (UUID)
     - Store LangGraph state snapshots

2. **Task API Endpoints**
   - Implement `api/routes/task.py`:
     - `POST /api/task`: Create new task from user intent
     - `GET /api/task/{taskId}/status`: Get task status
     - `GET /api/tasks`: List all tasks (optional, for debugging)
   - Add request/response validation
   - Add error handling (404 for missing tasks)

3. **Task State Management**
   - Define task states: `created`, `planning`, `running`, `completed`, `failed`, `paused`
   - Implement state transitions
   - Add timestamps for each state change
   - Store LangGraph execution checkpoints

### Acceptance Criteria
- [ ] Can create task via `POST /api/task` with intent
- [ ] Task ID is generated and returned
- [ ] Can retrieve task status via `GET /api/task/{taskId}/status`
- [ ] Task state persists in memory
- [ ] Proper error responses for invalid task IDs
- [ ] LangGraph state can be stored and retrieved

### Deliverables
- In-memory task storage
- Task CRUD endpoints
- Task state management
- LangGraph state persistence

---

## Phase 3: WebSocket Real-Time Updates

### Goal
Implement WebSocket connection for real-time agent updates to frontend.

### Tasks
1. **WebSocket Handler**
   - Implement `api/websocket.py`:
     - WebSocket endpoint: `/ws/task/{taskId}`
     - Connection manager for multiple clients
     - Task subscription model
     - Heartbeat/ping-pong for connection health

2. **Update Broadcasting**
   - Create `broadcast_update()` function:
     - Send updates to all clients subscribed to a task
     - Message types: `node_update`, `agent_status`, `task_complete`, `error`
   - Integrate with LangGraph node execution callbacks

3. **WebSocket Message Schemas**
   - Define message types in `core/schemas.py`:
     - `NodeUpdateMessage`: LangGraph node execution updates
     - `AgentStatusMessage`: Agent activity
     - `ErrorMessage`: Error notifications
     - `TaskCompleteMessage`: Task completion

### Acceptance Criteria
- [ ] WebSocket connection establishes successfully at `/ws/task/{taskId}`
- [ ] Client receives connection confirmation
- [ ] Can broadcast test messages to connected clients
- [ ] Connection closes gracefully
- [ ] Handles multiple concurrent connections
- [ ] LangGraph node updates broadcast in real-time

### Deliverables
- WebSocket endpoint
- Connection manager
- Message broadcasting system
- LangGraph callback integration

---

## Phase 4: LangGraph State Definition

### Goal
Define the LangGraph state schema that will be passed between nodes in the agent workflow.

### Tasks
1. **State Schema Design**
   - Implement `graph/state.py`:
     - `AgentState` TypedDict with fields:
       - `task_id`: Task identifier
       - `user_intent`: Original user input
       - `intent_analysis`: Parsed intent structure
       - `plan`: Execution plan
       - `current_step`: Current execution step
       - `context`: Shared context between agents
       - `company_data`: Research results
       - `icp_criteria`: ICP criteria from Notion
       - `icp_score`: Assessed ICP fit score
       - `crm_data`: HubSpot CRM data
       - `email_draft`: Generated email
       - `errors`: List of errors encountered
       - `requires_confirmation`: Flag for user confirmation
       - `confirmation_received`: User confirmation status

2. **State Reducers**
   - Implement state update functions:
     - `add_to_context()`: Merge new context data
     - `update_step()`: Move to next step
     - `add_error()`: Append error to error list

3. **State Annotations**
   - Use LangGraph Annotated types for state fields
   - Define reduction strategies (replace, append, merge)

### Acceptance Criteria
- [ ] AgentState TypedDict is properly defined
- [ ] State schema includes all required fields
- [ ] State reducers work correctly
- [ ] State can be serialized/deserialized

### Deliverables
- Complete AgentState definition
- State reducer functions
- State annotations

---

## Phase 5: LangChain Tools for Agents

### Goal
Create LangChain tool wrappers for each agent capability.

### Tasks
1. **Tool Base Structure**
   - Implement `graph/tools.py`:
     - Use LangChain `@tool` decorator
     - Create tools for each agent action

2. **Web Search Tools**
   - `research_company_tool`:
     - Input: company name
     - Output: company data (size, industry, funding)
   - `find_contacts_tool`:
     - Input: company name
     - Output: decision-maker list
   - `get_recent_news_tool`:
     - Input: company name
     - Output: recent news

3. **HubSpot CRM Tools**
   - `search_hubspot_company_tool`:
     - Input: company name
     - Output: HubSpot company record
   - `create_hubspot_company_tool`:
     - Input: company data
     - Output: Created company ID and URL
   - `create_hubspot_contact_tool`:
     - Input: contact data
     - Output: Created contact ID
   - `add_hubspot_note_tool`:
     - Input: record ID, note text
     - Output: Success confirmation

4. **Notion Tools**
   - `get_icp_criteria_tool`:
     - Input: None
     - Output: ICP criteria JSON
   - `get_notion_document_tool`:
     - Input: document ID/title
     - Output: Document content

5. **Email Drafting Tool**
   - `draft_email_tool`:
     - Input: recipient, context, intent
     - Output: Email subject and body

6. **Tool Integration**
   - Connect tools to agent implementations
   - Add error handling to each tool
   - Implement retry logic

### Acceptance Criteria
- [ ] All tools are decorated with @tool
- [ ] Tools have clear input/output schemas
- [ ] Tools can be called independently
- [ ] Tools integrate with agent implementations
- [ ] Error handling works for each tool

### Deliverables
- LangChain tool wrappers for all agents
- Tool schemas and documentation
- Error handling per tool

---

## Phase 6: Agent Implementations

### Goal
Implement concrete agent classes that use LangChain tools.

### Tasks
1. **Base Agent Class**
   - Implement `agents/base.py`:
     - `BaseAgent` abstract class
     - Common error handling
     - Logging support
     - Composio integration helpers

2. **Web Search Agent**
   - Implement `agents/web_search.py`:
     - Initialize Perplexity/SerpAPI client
     - Implement `research_company()` method
     - Implement `assess_icp_fit()` method
     - Fallback data for demo companies (Stripe, Notion, etc.)
     - Rate limit handling with exponential backoff

3. **HubSpot CRM Agent**
   - Implement `agents/hubspot.py`:
     - Initialize HubSpot API client
     - Implement CRM operations (create, search, update)
     - Mock CRM fallback for offline demos
     - Confirmation workflow support

4. **Notion Agent**
   - Implement `agents/notion.py`:
     - Initialize Notion API client
     - Fetch ICP criteria
     - Fetch documents by ID/title
     - Mock Notion data for offline demos

5. **Gmail Agent**
   - Implement `agents/gmail.py`:
     - Use LangChain ChatOpenAI for email drafting
     - Context-aware personalization
     - Tone adaptation based on sales stage
     - Email templates for different scenarios

### Acceptance Criteria
- [ ] All agents inherit from BaseAgent
- [ ] Each agent has working methods
- [ ] Agents can be called independently
- [ ] Mock/fallback data works for offline demos
- [ ] Error handling is robust

### Deliverables
- Complete agent implementations
- Mock data for all agents
- Error handling and retries

---

## Phase 7: LangGraph Node Functions

### Goal
Create LangGraph node functions that execute in the workflow graph.

### Tasks
1. **Node Implementation**
   - Implement `graph/nodes.py`:
     - Each node is a function that takes `AgentState` and returns updated state
     - Nodes should be pure functions where possible

2. **Core Nodes**
   - `analyze_intent_node(state)`:
     - Use LangChain LLM with structured output
     - Parse user intent
     - Extract entities (company names, contacts)
     - Update `intent_analysis` in state

   - `create_plan_node(state)`:
     - Use LLM to generate execution plan
     - Determine required agents and sequence
     - Update `plan` in state

   - `web_search_node(state)`:
     - Call Web Search Agent
     - Research company
     - Update `company_data` in state

   - `fetch_icp_node(state)`:
     - Call Notion Agent
     - Fetch ICP criteria
     - Update `icp_criteria` in state

   - `assess_icp_node(state)`:
     - Use company data + ICP criteria
     - Score ICP fit
     - Update `icp_score` in state

   - `check_icp_threshold_node(state)`:
     - Check if ICP score meets threshold
     - Set `requires_confirmation` if needed
     - Conditional routing logic

   - `create_crm_record_node(state)`:
     - Call HubSpot Agent
     - Create company record
     - Update `crm_data` in state

   - `draft_email_node(state)`:
     - Call Gmail Agent
     - Generate personalized email
     - Update `email_draft` in state

   - `search_crm_node(state)`:
     - Search HubSpot for existing records
     - Update `crm_data` in state

   - `await_confirmation_node(state)`:
     - Pause execution
     - Wait for user confirmation
     - Update `confirmation_received` in state

3. **Node Helpers**
   - Add logging to each node
   - Broadcast WebSocket updates from nodes
   - Error handling within nodes

### Acceptance Criteria
- [ ] All nodes are implemented as pure functions
- [ ] Nodes properly update AgentState
- [ ] Nodes can be tested independently
- [ ] WebSocket updates broadcast from nodes
- [ ] Error handling works in nodes

### Deliverables
- Complete set of LangGraph nodes
- Node testing capability
- WebSocket integration

---

## Phase 8: LangGraph Workflow Construction

### Goal
Build the LangGraph workflow that orchestrates the agent nodes.

### Tasks
1. **Workflow Graph Builder**
   - Implement `graph/workflow.py`:
     - Use `StateGraph` from LangGraph
     - Define nodes
     - Define edges and conditional routing
     - Compile the graph

2. **Lead Discovery Workflow**
   - Create `build_lead_discovery_graph()`:
     - Flow: Intent → Plan → Web Search → Fetch ICP → Assess ICP → Check Threshold → Confirmation → Create CRM
     - Nodes:
       1. `analyze_intent_node`
       2. `create_plan_node`
       3. `web_search_node`
       4. `fetch_icp_node`
       5. `assess_icp_node`
       6. `check_icp_threshold_node` (conditional)
       7. `await_confirmation_node` (if needed)
       8. `create_crm_record_node` (if confirmed)
     - Edges:
       - Sequential edges between main nodes
       - Conditional edge after `check_icp_threshold_node`:
         - If score < 6 → `await_confirmation_node`
         - If score >= 6 → `create_crm_record_node`
       - Conditional edge after `await_confirmation_node`:
         - If confirmed → `create_crm_record_node`
         - If rejected → END

3. **Email Drafting Workflow**
   - Create `build_email_drafting_graph()`:
     - Flow: Intent → Search CRM → Draft Email
     - Nodes:
       1. `analyze_intent_node`
       2. `search_crm_node`
       3. `draft_email_node`

4. **Pre-Meeting Prep Workflow**
   - Create `build_meeting_prep_graph()`:
     - Flow: Intent → Search CRM → Web Search → Compile Brief
     - Nodes:
       1. `analyze_intent_node`
       2. `search_crm_node`
       3. `web_search_node` (for recent news)
       4. `compile_brief_node`

5. **CRM Query Workflow**
   - Create `build_crm_query_graph()`:
     - Flow: Intent → Search CRM → Format Response
     - Nodes:
       1. `analyze_intent_node`
       2. `search_crm_node`

6. **Graph Compilation**
   - Compile each graph with checkpointer for state persistence
   - Add interrupt capability for confirmations

### Acceptance Criteria
- [ ] All workflow graphs build successfully
- [ ] Graphs have correct node connections
- [ ] Conditional routing works
- [ ] Graphs can be executed with sample state
- [ ] Checkpointing enables pause/resume

### Deliverables
- Complete LangGraph workflows for all flows
- Graph compilation logic
- Conditional routing implementation

---

## Phase 9: Workflow Executor Integration

### Goal
Integrate LangGraph workflows with FastAPI endpoints and task management.

### Tasks
1. **Workflow Executor**
   - Create `graph/executor.py`:
     - `execute_workflow()`: Run compiled graph
     - Determine which workflow to use based on intent
     - Stream updates via WebSocket
     - Handle interrupts for confirmations

2. **Intent Router**
   - Implement intent-based workflow selection:
     - "Research X" → Lead Discovery Workflow
     - "Draft email to Y" → Email Drafting Workflow
     - "Prepare for meeting with Z" → Meeting Prep Workflow
     - "What's the status of X deal?" → CRM Query Workflow

3. **Task Endpoint Integration**
   - Update `api/routes/task.py`:
     - `POST /api/task`: Create task and invoke workflow
     - Use LangGraph streaming for real-time updates
     - Store graph state in TaskStore

4. **Confirmation Handling**
   - Add endpoint: `POST /api/task/{taskId}/confirm`
   - Resume graph execution after confirmation
   - Update state with confirmation result

5. **WebSocket Streaming**
   - Stream LangGraph node executions to WebSocket
   - Broadcast each node start/complete
   - Send intermediate results

### Acceptance Criteria
- [ ] Workflows execute from API endpoints
- [ ] Intent routing selects correct workflow
- [ ] WebSocket streams node updates in real-time
- [ ] Confirmation workflow pauses and resumes correctly
- [ ] Task state persists between API calls

### Deliverables
- Workflow executor with streaming
- Intent-based routing
- Confirmation handling
- WebSocket integration

---

## Phase 10: LLM Integration for Planning & Reasoning

### Goal
Use LangChain's OpenAI integration for intent analysis, planning, and agent reasoning.

### Tasks
1. **LangChain LLM Setup**
   - Initialize `ChatOpenAI` in `core/config.py`
   - Configure for GPT-4o-mini (`gpt-4o-mini`) for cost-effective performance
   - Set temperature and model parameters
   - Note: Can upgrade to GPT-4o for complex reasoning if needed

2. **Structured Output for Intent**
   - Use LangChain's structured output with Pydantic:
     - Define `IntentSchema` for intent analysis
     - Use `with_structured_output()` method
     - Extract: task_type, entities, actions, parameters

3. **Structured Output for Planning**
   - Define `PlanSchema` for execution plans
   - Use LLM to generate plans with JSON schema
   - Validate plan structure

4. **Agent Reasoning with LLM**
   - ICP assessment reasoning:
     - Use LLM to analyze fit
     - Generate explanation for score
   - Email drafting:
     - Use LangChain prompt templates
     - Context injection from CRM
     - Tone adaptation

5. **Prompt Engineering**
   - Create prompt templates in `graph/prompts.py`:
     - Intent analysis prompts
     - Planning prompts
     - ICP assessment prompts
     - Email drafting prompts

### Acceptance Criteria
- [ ] LangChain ChatOpenAI initializes successfully
- [ ] Structured output returns valid Pydantic models
- [ ] Intent analysis extracts entities correctly
- [ ] Plan generation produces valid plans
- [ ] Email drafting generates quality emails

### Deliverables
- LangChain LLM integration
- Structured output schemas
- Prompt templates
- Intent and plan generation

---

## Phase 11: Composio Integration for External Tools

### Goal
Route external tool calls (HubSpot, Notion, Web Search) through Composio using MCPs.

### Tasks
1. **Composio Setup**
   - Install `composio-langchain` package
   - Configure Composio credentials in `.env`
   - Initialize Composio client in `core/config.py`

2. **Composio Tool Integration**
   - Update `graph/tools.py`:
     - Wrap Composio tools as LangChain tools
     - Use Composio MCPs for HubSpot, Notion
     - Implement retry/backoff via Composio

3. **MCP Adapters**
   - Create `utils/composio_adapters.py`:
     - `HubSpotMCP`: Wrapper for HubSpot operations via Composio
     - `NotionMCP`: Wrapper for Notion operations via Composio
     - Handle MCP error responses

4. **Agent Updates**
   - Update agents to use Composio MCPs:
     - `hubspot.py` → calls HubSpot via Composio
     - `notion.py` → calls Notion via Composio
   - Keep direct API as fallback for development

5. **Mock MCP Handlers**
   - Create in-memory MCP mock for offline/demo mode
   - Switch between real and mock MCPs via environment variable

### Acceptance Criteria
- [ ] Composio client initializes successfully
- [ ] MCP adapters work for HubSpot, Notion
- [ ] LangChain tools route through Composio
- [ ] Retry logic handles transient errors
- [ ] Mock MCPs available for offline demos

### Deliverables
- Composio integration
- MCP adapters for external tools
- Mock MCP handlers
- LangChain tool wrappers

---

## Phase 12: Error Handling & Resilience

### Goal
Implement robust error handling, retries, and graceful degradation.

### Tasks
1. **Retry Logic in LangGraph**
   - Add retry decorators to nodes
   - Exponential backoff for API calls
   - Max retry attempts configuration

2. **Error Node**
   - Create `error_handler_node(state)`:
     - Detect error type (transient vs permanent)
     - Decide retry or fail
     - Update error list in state

3. **Fallback Data System**
   - Create `utils/fallbacks.py`:
     - Hardcoded data for demo companies
     - Use when external APIs fail
     - Log when fallback is used

4. **Rate Limit Handling**
   - Detect rate limit errors (429 status)
   - Implement backoff with jitter
   - Cache responses when possible

5. **Graceful Degradation in Workflow**
   - Add conditional edges for error scenarios
   - Skip optional nodes if they fail
   - Provide partial results
   - Use LangGraph's error handling mechanisms

6. **Error Broadcasting**
   - Broadcast errors via WebSocket
   - Clear error messages for users
   - Suggested actions for recovery

### Acceptance Criteria
- [ ] Retry logic works for transient failures
- [ ] Rate limits trigger backoff
- [ ] Fallback data is used when APIs fail
- [ ] Error messages are clear and actionable
- [ ] Workflow continues despite non-critical errors
- [ ] Error states are captured in AgentState

### Deliverables
- Retry logic with backoff
- Error handling nodes
- Fallback data system
- Graceful degradation

---

## Phase 13: Performance Optimization

### Goal
Optimize for speed to meet <2 minute demo requirement.

### Tasks
1. **Parallel Node Execution in LangGraph**
   - Identify independent nodes
   - Use LangGraph parallel execution:
     - Run `web_search_node` and `fetch_icp_node` in parallel
   - Configure graph for parallelism

2. **Response Caching**
   - Implement caching layer:
     - Cache web search results (15-minute TTL)
     - Cache Notion documents (30-minute TTL)
     - Cache CRM queries (5-minute TTL)
   - Use LangChain cache

3. **Streaming Optimizations**
   - Stream LLM responses for email drafting
   - Show partial results as they arrive
   - Use LangChain streaming callbacks

4. **API Call Optimization**
   - Batch CRM operations when possible
   - Reduce redundant API calls
   - Use Composio caching

5. **Performance Monitoring**
   - Log execution time for each node
   - Track total workflow duration
   - Identify bottlenecks
   - Add performance metrics to WebSocket updates

### Acceptance Criteria
- [ ] Lead discovery flow completes in <2 minutes
- [ ] Independent nodes execute in parallel
- [ ] Caching reduces redundant API calls
- [ ] Performance logs show node timings
- [ ] Streaming provides responsive UX

### Deliverables
- Parallel LangGraph execution
- Response caching
- Performance monitoring
- Streaming optimizations

---

## Phase 14: Testing & Validation

### Goal
Test all workflows and ensure demo readiness.

### Tasks
1. **End-to-End Workflow Testing**
   - Test Flow 1: Lead Discovery & Qualification
     - "Research Stripe and assess ICP fit, then add to HubSpot"
   - Test Flow 2: Pre-Meeting Preparation
     - "Prepare me for my meeting with Acme Corp tomorrow"
   - Test Flow 3: Email Drafting
     - "Draft a follow-up email to john@acme.com"
   - Test Flow 4: Quick CRM Query
     - "What's the status of the Acme Corp deal?"

2. **LangGraph Testing**
   - Test each node independently
   - Test workflow compilation
   - Test conditional routing
   - Test interrupt/resume for confirmations
   - Test parallel execution

3. **Edge Case Testing**
   - Company not found by web search
   - Bad ICP fit score (confirmation workflow)
   - Contact not in CRM
   - API timeout/failure
   - Rate limiting
   - Invalid user input
   - LangGraph state corruption

4. **Performance Testing**
   - Time each workflow with stopwatch
   - Ensure all flows complete in <2 minutes
   - Optimize slow nodes

5. **Demo Data Preparation**
   - Create fallback data for 5 demo companies:
     - Stripe, Notion, Acme Corp, TechCorp, DataCo
   - Pre-populate mock CRM with sample data
   - Prepare sample ICP criteria in Notion mock

### Acceptance Criteria
- [ ] All 4 primary workflows work end-to-end
- [ ] Edge cases handled gracefully
- [ ] Performance meets <2 minute requirement
- [ ] Demo data is realistic and comprehensive
- [ ] No unhandled exceptions in logs
- [ ] LangGraph state transitions work correctly

### Deliverables
- Tested end-to-end workflows
- Edge case handling
- Demo data
- Performance validation

---

## Phase 15: Demo Preparation & Documentation

### Goal
Prepare the system for demo and document setup.

### Tasks
1. **Demo Script**
   - Create `backend/docs/DEMO_SCRIPT.md`:
     - Step-by-step demo walkthrough
     - Expected inputs and outputs
     - Talking points for each workflow
     - Fallback plans if something fails

2. **Setup Documentation**
   - Update `README.md`:
     - Installation instructions
     - Environment variable setup
     - How to run the backend
     - API endpoint documentation
     - LangGraph architecture overview

3. **API Documentation**
   - Add FastAPI automatic docs (Swagger UI)
   - Document all endpoints with examples
     - Include WebSocket connection instructions

4. **Architecture Documentation**
   - Create `backend/docs/ARCHITECTURE.md`:
     - LangGraph workflow diagrams
     - Node interaction flow
     - Data flow between nodes
     - Agent coordination explanation

5. **LangGraph Visualization**
   - Export LangGraph workflows as diagrams
   - Include in documentation
   - Show conditional routing visually

6. **Pre-Demo Checklist**
   - [ ] Run full demo 3 times successfully
   - [ ] Test with fresh environment
   - [ ] API keys loaded and working
   - [ ] Fallback data ready
   - [ ] WebSocket connection stable
   - [ ] Error handling tested
   - [ ] Performance within limits
   - [ ] LangGraph workflows visualized

### Acceptance Criteria
- [ ] Demo script is clear and comprehensive
- [ ] README has complete setup instructions
- [ ] API docs are auto-generated and accessible
- [ ] Architecture diagram shows LangGraph workflows
- [ ] Can run full demo offline using mocks
- [ ] Pre-demo checklist passes

### Deliverables
- Demo script
- Complete documentation
- API documentation
- Architecture diagram with LangGraph
- Workflow visualizations
- Pre-demo checklist

---

## Phase 16: Final Polish & Bug Fixes

### Goal
Final testing, bug fixes, and polish before submission.

### Tasks
1. **Bug Fixes**
   - Fix any remaining bugs from testing
   - Address edge cases
   - Improve error messages
   - Fix LangGraph state issues

2. **Code Cleanup**
   - Remove debug print statements
   - Clean up commented code
   - Ensure consistent code style
   - Add docstrings to nodes and workflows

3. **Logging Improvements**
   - Add structured logging
   - Log all node executions
   - Log execution times per node
   - Log errors with stack traces
   - LangGraph execution tracing

4. **Final Testing**
   - Run all test workflows 5 times each
   - Test with real APIs
   - Test with mock APIs
   - Test error scenarios
   - Test confirmation workflows
   - Test LangGraph interrupts

5. **Performance Final Check**
   - Verify <2 minute requirement
   - Optimize any slow nodes
   - Check memory usage
   - Ensure no memory leaks in LangGraph state

### Acceptance Criteria
- [ ] No critical bugs remaining
- [ ] Code is clean and documented
- [ ] Logging is comprehensive
- [ ] All tests pass consistently
- [ ] Performance requirements met
- [ ] LangGraph workflows are stable

### Deliverables
- Bug-free backend
- Clean, documented code
- Comprehensive logging
- Final performance validation
- Stable LangGraph workflows

---

## Execution Guidelines for AI Models

### How to Execute This Plan

1. **Sequential Execution**: Execute phases in order. Do not skip ahead.

2. **Completion Criteria**: Each phase must meet ALL acceptance criteria before moving to next phase.

3. **Testing**: Test each phase thoroughly before proceeding.

4. **Documentation**: Update README and inline comments as you build.

5. **Commit Strategy**: Commit after each phase completion with descriptive message.

6. **Error Handling**: If a phase fails, debug before proceeding.

### LangGraph Development Tips

1. **State-First Design**: Always define state schema before building nodes
2. **Pure Functions**: Keep nodes as pure functions when possible
3. **Test Nodes Independently**: Test each node with sample state before integration
4. **Visualize Workflows**: Use LangGraph visualization to debug routing
5. **Use Checkpointing**: Enable checkpointing for debugging and pause/resume
6. **Streaming**: Use streaming for real-time feedback to frontend

### Command Examples

```bash
# Start backend server
cd backend
python -m uvicorn main:app --reload --port 8000

# Run with environment variables
export OPENAI_API_KEY="sk-..."
export PERPLEXITY_API_KEY="..."
python -m uvicorn main:app --reload

# Test endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/task -H "Content-Type: application/json" -d '{"intent": "Research Stripe"}'

# Test WebSocket
wscat -c ws://localhost:8000/ws/task/task-123

# Visualize LangGraph workflow (in Python)
from graph.workflow import build_lead_discovery_graph
graph = build_lead_discovery_graph()
graph.get_graph().draw_mermaid_png(output_file_path="workflow.png")
```

### Key Milestones

- **Milestone 1** (End of Phase 4): LangGraph state defined
- **Milestone 2** (End of Phase 7): All LangGraph nodes implemented
- **Milestone 3** (End of Phase 8): Complete workflows working
- **Milestone 4** (End of Phase 10): LLM integration complete
- **Milestone 5** (End of Phase 14): Demo-ready system
- **Milestone 6** (End of Phase 16): Submission-ready

### Priority Levels

- **P0 (Critical)**: Phases 1-10, 14, 15 - Must have for demo
- **P1 (High)**: Phases 11, 12, 13 - Important for robustness
- **P2 (Nice to have)**: Phase 16 polish - Can defer if time constrained

### Time Estimates

- Phases 1-3: 6 hours (Foundation & WebSocket)
- Phases 4-5: 4 hours (LangGraph state & tools)
- Phases 6-8: 12 hours (Agents & workflows)
- Phases 9-10: 8 hours (Integration & LLM)
- Phases 11-13: 8 hours (Composio, errors, performance)
- Phases 14-16: 10 hours (Testing & polish)
- **Total**: ~48 hours (hackathon timeline)

---

## Success Criteria

### Minimum Viable Demo
- User inputs "Research Stripe and assess ICP fit"
- LangGraph executes lead discovery workflow
- Web Search node finds Stripe data
- Notion node gets ICP criteria
- ICP assessment node scores fit and provides reasoning
- Conditional routing based on score
- User confirmation workflow (if needed)
- HubSpot node creates record
- Total time: <2 minutes

### Stretch Goals
- All 4 workflows operational
- Email drafting with quality context
- Pre-meeting brief generation
- Real API integrations (not mocks)
- Beautiful error handling
- Performance consistently under 90 seconds
- LangGraph visualization in UI

---

## LangGraph Architecture Overview

### Why LangGraph?
- **State Management**: Built-in state passing between nodes
- **Conditional Routing**: Easy branching logic (ICP threshold, confirmations)
- **Checkpointing**: Pause/resume for user confirmations
- **Streaming**: Real-time updates to frontend
- **Debugging**: Graph visualization and execution tracing
- **Flexibility**: Dynamic workflows that can adapt at runtime

### Workflow Pattern
```
User Intent
    ↓
Analyze Intent (LLM)
    ↓
Create Plan (LLM)
    ↓
Execute Nodes (Agents)
    ↓ (conditional routing)
Confirmation Check
    ↓
Final Action (CRM write, email draft, etc.)
    ↓
Return Results
```

### Node Types
1. **LLM Nodes**: Use LangChain for reasoning (intent, planning, assessment)
2. **Tool Nodes**: Call external APIs (Web Search, HubSpot, Notion)
3. **Logic Nodes**: Conditional checks and routing
4. **Confirmation Nodes**: Interrupt and wait for user input

---

## Emergency Fallbacks

If short on time, prioritize:
1. Lead discovery workflow (Flow 1) - MUST WORK
2. Mock agents over real APIs (faster to implement)
3. Basic conditional routing over complex dynamic planning
4. Manual confirmation over automatic orchestration
5. Cached responses over live API calls

## Notes for AI Model Execution

- **LangGraph First**: Build and test LangGraph workflows early
- **State is King**: All data flows through AgentState
- **Visualize Often**: Use graph visualization to debug
- **Test Nodes**: Test each node independently before chaining
- **Stream Everything**: Use streaming for responsive UX
- **Checkpoint for Confirmations**: Use interrupts for user input
- **Document Workflows**: Comment your graph construction logic
- **Error Boundaries**: Add error handling at node level
- **Parallel When Possible**: Use LangGraph parallelism for speed
