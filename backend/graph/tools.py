"""LangChain tools for agents."""
from typing import Dict, Any, Optional
from langchain.tools import tool
from agents.hubspot_composio import HubSpotComposioAgent
from agents.notion import NotionAgent
from core.config import Config
import logging

logger = logging.getLogger(__name__)

# Initialize agents
_hubspot_agent = None
_notion_agent = None


def get_hubspot_agent() -> HubSpotComposioAgent:
    """Get or create HubSpot Composio agent instance."""
    global _hubspot_agent
    if _hubspot_agent is None:
        use_mock = Config.USE_MOCK_MCP
        _hubspot_agent = HubSpotComposioAgent(use_mock=use_mock)
    return _hubspot_agent


def get_notion_agent() -> NotionAgent:
    """Get or create Notion agent instance."""
    global _notion_agent
    if _notion_agent is None:
        _notion_agent = NotionAgent()
    return _notion_agent


# HubSpot CRM Tools

@tool
async def search_hubspot_company_tool(company_name: str) -> Dict[str, Any]:
    """
    Search for a company in HubSpot CRM.

    Args:
        company_name: Name of the company to search for

    Returns:
        Dictionary with company data if found, or indication that company was not found
    """
    agent = get_hubspot_agent()
    return await agent.search_company(company_name)


@tool
async def create_hubspot_company_tool(
    name: str,
    domain: Optional[str] = None,
    industry: Optional[str] = None,
    description: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    country: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new company in HubSpot CRM.

    Args:
        name: Company name (required)
        domain: Company website domain
        industry: Company industry
        description: Company description
        city: Company city
        state: Company state/province
        country: Company country

    Returns:
        Dictionary with created company data including ID and URL
    """
    company_data = {
        "name": name,
        "domain": domain or "",
        "industry": industry or "",
        "description": description or "",
        "city": city or "",
        "state": state or "",
        "country": country or ""
    }

    agent = get_hubspot_agent()
    return await agent.create_company(company_data)


@tool
async def create_hubspot_contact_tool(
    email: str,
    firstname: Optional[str] = None,
    lastname: Optional[str] = None,
    company: Optional[str] = None,
    jobtitle: Optional[str] = None,
    phone: Optional[str] = None,
    company_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new contact in HubSpot CRM.

    Args:
        email: Contact email (required)
        firstname: Contact first name
        lastname: Contact last name
        company: Company name
        jobtitle: Job title
        phone: Phone number
        company_id: HubSpot company ID to associate with

    Returns:
        Dictionary with created contact data including ID
    """
    contact_data = {
        "email": email,
        "firstname": firstname or "",
        "lastname": lastname or "",
        "company": company or "",
        "jobtitle": jobtitle or "",
        "phone": phone or ""
    }

    agent = get_hubspot_agent()
    return await agent.create_contact(contact_data, company_id)


@tool
async def add_hubspot_note_tool(
    record_id: str,
    note_text: str,
    record_type: str = "company"
) -> Dict[str, Any]:
    """
    Add a note to a HubSpot company or contact record.

    Args:
        record_id: ID of the company or contact
        note_text: The note content to add
        record_type: Type of record - "company" or "contact" (default: "company")

    Returns:
        Dictionary indicating success or failure
    """
    agent = get_hubspot_agent()
    return await agent.add_note(record_id, note_text, record_type)


@tool
async def add_hubspot_research_note_tool(
    company_id: str,
    company_data: Optional[Dict[str, Any]] = None,
    icp_score: Optional[int] = None,
    icp_reasoning: Optional[str] = None,
    recent_news: Optional[list] = None
) -> Dict[str, Any]:
    """
    Add a formatted research note to a HubSpot company record.

    Args:
        company_id: HubSpot company ID
        company_data: Dictionary with company research data (industry, size, funding, etc.)
        icp_score: ICP fit score (0-10)
        icp_reasoning: Explanation of ICP score
        recent_news: List of recent news items

    Returns:
        Dictionary indicating success or failure
    """
    research_data = {}

    if company_data:
        research_data["company_data"] = company_data
    if icp_score is not None:
        research_data["icp_score"] = icp_score
    if icp_reasoning:
        research_data["icp_reasoning"] = icp_reasoning
    if recent_news:
        research_data["recent_news"] = recent_news

    agent = get_hubspot_agent()
    return await agent.add_research_note(company_id, research_data)


# Notion Tools

@tool
async def get_icp_criteria_tool() -> Dict[str, Any]:
    """
    Fetch ICP (Ideal Customer Profile) criteria from Notion.

    Returns:
        Dictionary containing ICP criteria including:
        - company_size: Min/max employee range
        - industries: List of target industries
        - funding_stage: List of acceptable funding stages
        - geography: List of target regions
        - growth_indicators: List of growth signals
    """
    agent = get_notion_agent()
    # Assuming NotionAgent has a get_icp_criteria method
    # If not implemented yet, this will need to be added
    try:
        return await agent.get_icp_criteria()
    except AttributeError:
        logger.warning("NotionAgent.get_icp_criteria not implemented, returning mock data")
        return {
            "success": True,
            "criteria": {
                "company_size": {"min": 50, "max": 5000},
                "industries": ["Technology", "SaaS", "E-commerce", "Financial Services"],
                "funding_stage": ["Series A", "Series B", "Series C", "Series D+"],
                "geography": ["North America", "Europe", "Asia-Pacific"],
                "growth_indicators": [
                    "YoY revenue growth > 50%",
                    "Recent funding round",
                    "Expanding internationally"
                ]
            }
        }


@tool
async def get_notion_document_tool(document_id: str) -> Dict[str, Any]:
    """
    Fetch a Notion document by ID.

    Args:
        document_id: Notion page/document ID

    Returns:
        Dictionary with document content
    """
    agent = get_notion_agent()
    try:
        return await agent.get_document(document_id)
    except AttributeError:
        logger.warning("NotionAgent.get_document not implemented")
        return {
            "success": False,
            "error": "NotionAgent.get_document not implemented"
        }


# Export all tools as a list for easy registration
HUBSPOT_TOOLS = [
    search_hubspot_company_tool,
    create_hubspot_company_tool,
    create_hubspot_contact_tool,
    add_hubspot_note_tool,
    add_hubspot_research_note_tool
]

NOTION_TOOLS = [
    get_icp_criteria_tool,
    get_notion_document_tool
]

ALL_TOOLS = HUBSPOT_TOOLS + NOTION_TOOLS
