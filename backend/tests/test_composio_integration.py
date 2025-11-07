"""
Test script for Composio HubSpot integration.

This script tests the Composio MCP adapter and HubSpot agent
in both mock and real modes.

Usage:
    # Test with mock data (no API keys required)
    python -m tests.test_composio_integration --mock

    # Test with real Composio API (requires COMPOSIO_API_KEY)
    python -m tests.test_composio_integration --real
"""
import asyncio
import sys
import argparse
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.composio_adapters import HubSpotMCP, NotionMCP
from agents.hubspot_composio import HubSpotComposioAgent
from core.config import Config


async def test_hubspot_mcp(use_mock: bool = True):
    """Test HubSpot MCP adapter."""
    print("\n" + "="*60)
    print(f"Testing HubSpot MCP Adapter (Mock Mode: {use_mock})")
    print("="*60)

    mcp = HubSpotMCP(use_mock=use_mock)

    # Test 1: Search for existing company
    print("\n[Test 1] Searching for company 'Stripe'...")
    result = await mcp.search_company("Stripe")
    if result:
        print(f"✅ Found company: {result.get('name')}")
        print(f"   ID: {result.get('id')}")
        print(f"   Domain: {result.get('domain')}")
    else:
        print("❌ Company not found")

    # Test 2: Search for non-existent company
    print("\n[Test 2] Searching for company 'NonExistentCompany123'...")
    result = await mcp.search_company("NonExistentCompany123")
    if result:
        print(f"⚠️  Unexpectedly found company: {result}")
    else:
        print("✅ Company not found (as expected)")

    # Test 3: Create a new company
    print("\n[Test 3] Creating new company 'Test Corp'...")
    company_data = {
        "name": "Test Corp",
        "domain": "testcorp.com",
        "industry": "Technology",
        "description": "Test company for integration testing"
    }
    result = await mcp.create_company(company_data)
    if result and result.get("id"):
        print(f"✅ Created company: {result.get('name')}")
        print(f"   ID: {result.get('id')}")
        print(f"   URL: {result.get('url')}")
        company_id = result.get('id')
    else:
        print("❌ Failed to create company")
        company_id = None

    # Test 4: Create a contact
    print("\n[Test 4] Creating new contact...")
    contact_data = {
        "email": "john.doe@testcorp.com",
        "firstname": "John",
        "lastname": "Doe",
        "company": "Test Corp",
        "jobtitle": "CEO"
    }
    result = await mcp.create_contact(contact_data)
    if result and result.get("id"):
        print(f"✅ Created contact: {contact_data['email']}")
        print(f"   ID: {result.get('id')}")
    else:
        print("❌ Failed to create contact")

    # Test 5: Add a note
    if company_id:
        print("\n[Test 5] Adding note to company...")
        note_text = "This is a test note added via Composio MCP integration."
        success = await mcp.add_note(company_id, note_text, "company")
        if success:
            print("✅ Note added successfully")
        else:
            print("❌ Failed to add note")

    print("\n" + "="*60)
    print("HubSpot MCP Tests Complete")
    print("="*60)


async def test_hubspot_agent(use_mock: bool = True):
    """Test HubSpot Composio Agent."""
    print("\n" + "="*60)
    print(f"Testing HubSpot Composio Agent (Mock Mode: {use_mock})")
    print("="*60)

    agent = HubSpotComposioAgent(use_mock=use_mock)

    # Test 1: Search for company
    print("\n[Test 1] Agent: Search for company 'Notion'...")
    result = await agent.search_company("Notion")
    print(f"   Success: {result.get('success')}")
    print(f"   Found: {result.get('found')}")
    if result.get('found'):
        print(f"   Company: {result.get('company', {}).get('name')}")

    # Test 2: Create company with duplicate check
    print("\n[Test 2] Agent: Create company 'Acme Corp' (with duplicate check)...")
    company_data = {
        "name": "Acme Corp",
        "domain": "acme.com",
        "industry": "E-commerce",
        "description": "Leading e-commerce platform"
    }
    result = await agent.create_company(company_data, check_existing=True)
    print(f"   Success: {result.get('success')}")
    print(f"   Created: {result.get('created')}")
    print(f"   Message: {result.get('message')}")
    company_id = result.get('company', {}).get('id')

    # Test 3: Add research note
    if company_id:
        print("\n[Test 3] Agent: Add research note to company...")
        research_data = {
            "company_data": {
                "industry": "E-commerce",
                "size": "500 employees",
                "funding": "Series C - $50M"
            },
            "icp_score": 8,
            "icp_reasoning": "Strong fit: right size, growing fast, in target industry",
            "recent_news": [
                "Launched new AI-powered product recommendation engine",
                "Expanded to European markets",
                "Named as one of the fastest-growing e-commerce platforms"
            ]
        }
        result = await agent.add_research_note(company_id, research_data)
        print(f"   Success: {result.get('success')}")
        print(f"   Message: {result.get('message')}")

    # Test 4: Create company with contacts
    print("\n[Test 4] Agent: Create company with multiple contacts...")
    company_data = {
        "name": "DataCo Analytics",
        "domain": "dataco.io",
        "industry": "Data Analytics",
        "description": "Enterprise data analytics platform"
    }
    contacts = [
        {
            "email": "sarah@dataco.io",
            "firstname": "Sarah",
            "lastname": "Johnson",
            "jobtitle": "CEO"
        },
        {
            "email": "mike@dataco.io",
            "firstname": "Mike",
            "lastname": "Chen",
            "jobtitle": "VP of Sales"
        }
    ]
    result = await agent.create_company_with_contacts(company_data, contacts)
    print(f"   Success: {result.get('success')}")
    print(f"   Contacts Created: {result.get('contacts_created')}")
    print(f"   Message: {result.get('message')}")

    print("\n" + "="*60)
    print("HubSpot Agent Tests Complete")
    print("="*60)


async def test_notion_mcp(use_mock: bool = True):
    """Test Notion MCP adapter."""
    print("\n" + "="*60)
    print(f"Testing Notion MCP Adapter (Mock Mode: {use_mock})")
    print("="*60)

    mcp = NotionMCP(use_mock=use_mock)

    # Test 1: Get ICP criteria
    print("\n[Test 1] Fetching ICP criteria...")
    result = await mcp.get_icp_criteria()
    if result:
        print("✅ Retrieved ICP criteria:")
        print(f"   Company Size: {result.get('company_size')}")
        print(f"   Industries: {', '.join(result.get('industries', []))}")
        print(f"   Funding Stages: {', '.join(result.get('funding_stage', []))}")
    else:
        print("❌ Failed to retrieve ICP criteria")

    # Test 2: Get document
    print("\n[Test 2] Fetching Notion document...")
    result = await mcp.get_document("test-doc-123")
    if result:
        print(f"✅ Retrieved document: {result.get('title')}")
    else:
        print("❌ Failed to retrieve document")

    print("\n" + "="*60)
    print("Notion MCP Tests Complete")
    print("="*60)


async def test_langchain_tools(use_mock: bool = True):
    """Test LangChain tool wrappers."""
    print("\n" + "="*60)
    print(f"Testing LangChain Tools (Mock Mode: {use_mock})")
    print("="*60)

    # Set config for mock mode
    if use_mock:
        import os
        os.environ['USE_MOCK_MCP'] = 'true'

    from graph.tools import (
        search_hubspot_company_tool,
        create_hubspot_company_tool,
        get_icp_criteria_tool
    )

    # Test 1: Search tool
    print("\n[Test 1] LangChain Tool: search_hubspot_company_tool")
    result = await search_hubspot_company_tool.ainvoke({"company_name": "Stripe"})
    print(f"   Result: {result.get('found')} - {result.get('company', {}).get('name')}")

    # Test 2: Create company tool
    print("\n[Test 2] LangChain Tool: create_hubspot_company_tool")
    result = await create_hubspot_company_tool.ainvoke({
        "name": "TechStart Inc",
        "domain": "techstart.io",
        "industry": "SaaS"
    })
    print(f"   Success: {result.get('success')}")
    print(f"   Message: {result.get('message')}")

    # Test 3: ICP criteria tool
    print("\n[Test 3] LangChain Tool: get_icp_criteria_tool")
    result = await get_icp_criteria_tool.ainvoke({})
    print(f"   Success: {result.get('success')}")
    if result.get('criteria'):
        print(f"   Industries: {len(result['criteria'].get('industries', []))} industries")

    print("\n" + "="*60)
    print("LangChain Tools Tests Complete")
    print("="*60)


async def run_all_tests(use_mock: bool = True):
    """Run all integration tests."""
    print("\n" + "="*60)
    print("COMPOSIO INTEGRATION TEST SUITE")
    print("="*60)
    print(f"Mode: {'MOCK (No API calls)' if use_mock else 'REAL (API calls)'}")
    print("="*60)

    try:
        # Test HubSpot MCP
        await test_hubspot_mcp(use_mock)

        # Test HubSpot Agent
        await test_hubspot_agent(use_mock)

        # Test Notion MCP
        await test_notion_mcp(use_mock)

        # Test LangChain tools
        await test_langchain_tools(use_mock)

        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*60)

    except Exception as e:
        print("\n" + "="*60)
        print(f"❌ TEST FAILED: {e}")
        print("="*60)
        import traceback
        traceback.print_exc()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Test Composio HubSpot integration')
    parser.add_argument('--mock', action='store_true', help='Use mock mode (no API calls)')
    parser.add_argument('--real', action='store_true', help='Use real API mode (requires API keys)')

    args = parser.parse_args()

    # Default to mock mode if neither flag is specified
    use_mock = True
    if args.real:
        use_mock = False
        print("\n⚠️  Real API mode selected. Ensure you have set:")
        print("   - COMPOSIO_API_KEY (or USE_COMPOSIO=false)")
        print("   - HUBSPOT_API_KEY (if not using Composio)")
        print("   - NOTION_API_KEY (if not using Composio)")
        print()

    asyncio.run(run_all_tests(use_mock))


if __name__ == "__main__":
    main()
