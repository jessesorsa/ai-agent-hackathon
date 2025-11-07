# Testing the Composio Integration

This directory contains tests for the Composio HubSpot integration.

## Quick Test (No API Keys Required)

Test with mock data - no external API calls:

```bash
cd backend
python -m tests.test_composio_integration --mock
```

This will test:
- ✅ HubSpot MCP adapter (search, create, notes)
- ✅ HubSpot Composio Agent (all operations)
- ✅ Notion MCP adapter (ICP criteria, documents)
- ✅ LangChain tool wrappers

## Test with Real APIs

To test with real Composio API calls:

1. Set up your environment variables in `.env`:
   ```bash
   COMPOSIO_API_KEY=your-key-here
   USE_COMPOSIO=true
   USE_MOCK_MCP=false
   ```

2. Run the tests:
   ```bash
   python -m tests.test_composio_integration --real
   ```

## What Gets Tested

### HubSpot MCP Adapter
- Search for companies (existing and non-existent)
- Create new companies
- Create contacts
- Add notes to records

### HubSpot Composio Agent
- Search operations
- Create company with duplicate checking
- Add formatted research notes
- Bulk operations (company + contacts)

### Notion MCP Adapter
- Fetch ICP criteria
- Get documents by ID

### LangChain Tools
- Tool wrappers for all operations
- Proper async invocation
- Correct response formats

## Expected Output

```
============================================================
COMPOSIO INTEGRATION TEST SUITE
============================================================
Mode: MOCK (No API calls)
============================================================

============================================================
Testing HubSpot MCP Adapter (Mock Mode: True)
============================================================

[Test 1] Searching for company 'Stripe'...
✅ Found company: Stripe
   ID: mock-stripe-001
   Domain: stripe.com

[Test 2] Searching for company 'NonExistentCompany123'...
✅ Company not found (as expected)

...

============================================================
✅ ALL TESTS COMPLETED SUCCESSFULLY
============================================================
```

## Integration with CI/CD

You can add these tests to your CI pipeline:

```yaml
# .github/workflows/test.yml
- name: Test Composio Integration
  run: |
    cd backend
    python -m tests.test_composio_integration --mock
```
