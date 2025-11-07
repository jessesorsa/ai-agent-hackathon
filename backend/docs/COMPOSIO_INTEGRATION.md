# Composio HubSpot Integration via MCP

This document describes the Composio integration for routing HubSpot and Notion operations through Model Context Protocol (MCP).

## Overview

The implementation adds a layer that routes external tool calls (HubSpot CRM, Notion) through Composio's MCP, providing:
- Unified credential management
- Automatic retry logic
- Rate limiting handling
- Mock mode for offline demos
- Centralized error handling

## Architecture

```
LangGraph Workflow
    ↓
LangChain Tools (graph/tools.py)
    ↓
HubSpot Composio Agent (agents/hubspot_composio.py)
    ↓
HubSpot MCP Adapter (utils/composio_adapters.py)
    ↓
Composio MCP ←→ HubSpot API
```

## Components

### 1. MCP Adapters (`utils/composio_adapters.py`)

**HubSpotMCP:**
- `search_company(company_name)` - Search for companies in CRM
- `create_company(company_data)` - Create new company records
- `create_contact(contact_data)` - Create new contacts
- `add_note(record_id, note_text)` - Add notes to records
- Mock implementations for all operations

**NotionMCP:**
- `get_icp_criteria()` - Fetch ICP criteria from Notion
- `get_document(document_id)` - Get Notion documents
- Mock implementations for offline demos

### 2. Agent Implementation (`agents/hubspot_composio.py`)

**HubSpotComposioAgent:**
- Extends `BaseAgent` with MCP integration
- Methods:
  - `search_company(company_name)`
  - `create_company(company_data, check_existing=True)`
  - `create_contact(contact_data, company_id=None)`
  - `add_note(record_id, note_text, record_type="company")`
  - `add_research_note(company_id, research_data)`
  - `create_company_with_contacts(company_data, contacts)`
- Built-in error handling and logging
- Automatic duplicate checking
- Formatted research notes

### 3. LangChain Tools (`graph/tools.py`)

**HubSpot Tools:**
- `search_hubspot_company_tool`
- `create_hubspot_company_tool`
- `create_hubspot_contact_tool`
- `add_hubspot_note_tool`
- `add_hubspot_research_note_tool`

**Notion Tools:**
- `get_icp_criteria_tool`
- `get_notion_document_tool`

All tools are async and follow LangChain's `@tool` decorator pattern.

### 4. Configuration (`core/config.py`)

New settings:
```python
COMPOSIO_API_KEY: str          # Composio API key
USE_COMPOSIO: bool             # Enable/disable Composio routing
USE_MOCK_MCP: bool             # Use mock data for demos
HUBSPOT_API_KEY: str           # Fallback direct API key
NOTION_API_KEY: str            # Fallback direct API key
```

Helper method:
```python
Config.get_composio_client()  # Returns ComposioToolSet instance
```

## Usage

### Environment Setup

```bash
# .env file
COMPOSIO_API_KEY=your-composio-key
USE_COMPOSIO=true
USE_MOCK_MCP=false  # Set to true for offline demos
```

### Using in LangGraph Workflows

```python
from graph.tools import HUBSPOT_TOOLS, create_hubspot_company_tool

# In a LangGraph node
async def create_crm_record_node(state: AgentState):
    company_data = state.get("company_data")

    result = await create_hubspot_company_tool.ainvoke({
        "name": company_data["name"],
        "domain": company_data.get("domain"),
        "industry": company_data.get("industry"),
        "description": company_data.get("description")
    })

    if result["success"]:
        state["crm_data"] = result["company"]

    return state
```

### Direct Agent Usage

```python
from agents.hubspot_composio import HubSpotComposioAgent

# Initialize agent
agent = HubSpotComposioAgent(use_mock=False)

# Search for company
result = await agent.search_company("Stripe")
if result["found"]:
    company = result["company"]

# Create company with duplicate check
result = await agent.create_company({
    "name": "Acme Corp",
    "domain": "acme.com",
    "industry": "E-commerce"
}, check_existing=True)

# Add research note
await agent.add_research_note(company_id, {
    "company_data": {...},
    "icp_score": 8,
    "icp_reasoning": "Strong fit...",
    "recent_news": [...]
})
```

### Mock Mode for Demos

```python
# Use mock mode (no API calls)
agent = HubSpotComposioAgent(use_mock=True)

# Will return mock data for demo companies
result = await agent.search_company("Stripe")
# Returns: {'id': 'mock-stripe-001', 'name': 'Stripe', ...}
```

## Testing

See [tests/TESTING_GUIDE.md](../tests/TESTING_GUIDE.md) for comprehensive testing instructions.

### Quick Test

```bash
cd backend
python3 -m tests.test_composio_integration --mock
```

This runs all integration tests without requiring API keys.

## Integration with Implementation Plan

This implementation satisfies **Phase 11: Composio Integration for External Tools** from the implementation plan:

- ✅ Composio setup and initialization
- ✅ HubSpot MCP adapter
- ✅ Notion MCP adapter
- ✅ LangChain tool wrappers
- ✅ Agent updates to use Composio MCPs
- ✅ Mock MCP handlers for offline demos
- ✅ Error handling and retry logic

## Benefits

1. **Centralized Tool Management:** All external API calls go through Composio
2. **Credential Security:** API keys managed by Composio, not hardcoded
3. **Automatic Retries:** Built-in retry logic with exponential backoff
4. **Rate Limiting:** Composio handles rate limits across all tools
5. **Mock Mode:** Easy offline demos without real API calls
6. **Observability:** Centralized logging and monitoring through Composio
7. **Easy Testing:** Mock implementations for all operations

## Error Handling

All operations return standardized response format:

```python
{
    "success": bool,
    "error": str,           # If success=False
    "agent": str,           # Agent name
    # ... operation-specific data
}
```

Errors are logged and gracefully handled at multiple levels:
1. MCP adapter level
2. Agent level
3. LangChain tool level

## Future Enhancements

- [ ] Add more HubSpot operations (deals, tasks, emails)
- [ ] Support for more Notion operations
- [ ] Caching layer for frequently accessed data
- [ ] Webhook support for real-time updates
- [ ] Performance metrics and monitoring
- [ ] Batch operations for efficiency

## Migration from Direct API

If you have existing code using direct HubSpot API calls:

```python
# Before (direct API)
from agents.hubspot import HubSpotAgent
agent = HubSpotAgent()

# After (via Composio)
from agents.hubspot_composio import HubSpotComposioAgent
agent = HubSpotComposioAgent()

# API stays the same!
result = await agent.search_company("Stripe")
```

The API is designed to be compatible, so migration is seamless.
