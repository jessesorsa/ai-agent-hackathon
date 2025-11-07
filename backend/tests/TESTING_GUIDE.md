# Testing Guide for Composio Integration

## Prerequisites

Before testing, ensure you have the dependencies installed:

```bash
cd backend
pip install -r requirements.txt
```

## Testing Steps

### 1. Quick Syntax Check

Verify the Python files have no syntax errors:

```bash
# Check MCP adapters
python3 -m py_compile utils/composio_adapters.py

# Check HubSpot agent
python3 -m py_compile agents/hubspot_composio.py

# Check LangChain tools
python3 -m py_compile graph/tools.py
```

### 2. Run Integration Tests (Mock Mode)

Test without making any real API calls:

```bash
cd backend
python3 -m tests.test_composio_integration --mock
```

**Expected output:**
- All HubSpot MCP operations should work with mock data
- All agent methods should execute successfully
- All LangChain tools should invoke correctly

### 3. Run Integration Tests (Real API Mode)

⚠️ **Only after setting up API keys!**

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set:
   ```bash
   OPENAI_API_KEY=sk-your-key-here
   COMPOSIO_API_KEY=your-composio-key
   USE_COMPOSIO=true
   USE_MOCK_MCP=false
   ```

3. Run tests:
   ```bash
   python3 -m tests.test_composio_integration --real
   ```

### 4. Manual Testing with Python REPL

You can also test individual components interactively:

```python
# Start Python REPL from backend directory
cd backend
python3

# Test HubSpot MCP in mock mode
import asyncio
from utils.composio_adapters import HubSpotMCP

async def test():
    mcp = HubSpotMCP(use_mock=True)
    result = await mcp.search_company("Stripe")
    print(result)

asyncio.run(test())
```

### 5. Test with FastAPI Server

Start the server and test via HTTP:

```bash
# Start server
cd backend
uvicorn main:app --reload --port 8000
```

Then in another terminal:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test creating a task that uses HubSpot
curl -X POST http://localhost:8000/api/task \
  -H "Content-Type: application/json" \
  -d '{"intent": "Research Stripe and add to HubSpot"}'
```

## Troubleshooting

### ModuleNotFoundError: No module named 'composio_langchain'

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### ImportError: cannot import name 'HubSpotComposioAgent'

**Solution:** Ensure you're running from the `backend` directory:
```bash
cd backend
python3 -m tests.test_composio_integration --mock
```

### Composio API errors

**Solution:** Check if you're in mock mode or verify your API key:
```bash
# Use mock mode (no API needed)
export USE_MOCK_MCP=true
python3 -m tests.test_composio_integration --mock
```

## Success Criteria

✅ **All tests should show:**
- Companies can be searched (mock or real)
- Companies can be created
- Contacts can be created
- Notes can be added
- Agent operations work correctly
- LangChain tools invoke without errors

## Next Steps After Testing

1. **If tests pass:** Safe to merge your branch
2. **If tests fail:** Review error messages and fix issues
3. **Integration testing:** Test with the full LangGraph workflow
4. **End-to-end testing:** Test complete user flows through the API
