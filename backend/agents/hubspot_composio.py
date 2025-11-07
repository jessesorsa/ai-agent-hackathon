"""HubSpot CRM Agent using Composio MCP integration."""
import logging
from typing import Any, Dict, Optional, List
from agents.base import BaseAgent
from utils.composio_adapters import HubSpotMCP

logger = logging.getLogger(__name__)


class HubSpotComposioAgent(BaseAgent):
    """
    HubSpot CRM Agent that routes operations through Composio MCP.

    This agent handles all HubSpot CRM operations including:
    - Searching for companies and contacts
    - Creating new companies and contacts
    - Adding notes and activities
    - Managing confirmation workflows
    """

    def __init__(self, use_mock: bool = False):
        """
        Initialize HubSpot Composio Agent.

        Args:
            use_mock: If True, use mock data instead of real API calls
        """
        super().__init__(name="HubSpot Composio Agent")
        self.mcp = HubSpotMCP(use_mock=use_mock)
        self.log_info("HubSpot Composio Agent initialized")

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a HubSpot CRM action via Composio MCP.

        Args:
            action: The action to perform (search_company, create_company, etc.)
            **kwargs: Action-specific parameters

        Returns:
            Dictionary with execution results
        """
        try:
            self.log_info(f"Executing action: {action}")

            if action == "search_company":
                return await self.search_company(**kwargs)
            elif action == "create_company":
                return await self.create_company(**kwargs)
            elif action == "create_contact":
                return await self.create_contact(**kwargs)
            elif action == "add_note":
                return await self.add_note(**kwargs)
            else:
                return {
                    "success": False,
                    "error": f"Unknown action: {action}",
                    "agent": self.name
                }

        except Exception as e:
            return self.handle_error(e, context={"action": action, "kwargs": kwargs})

    async def search_company(self, company_name: str) -> Dict[str, Any]:
        """
        Search for a company in HubSpot CRM.

        Args:
            company_name: Name of the company to search for

        Returns:
            Dictionary with search results
        """
        try:
            self.log_info(f"Searching for company: {company_name}")

            result = await self.mcp.search_company(company_name)

            if result:
                return {
                    "success": True,
                    "found": True,
                    "company": result,
                    "agent": self.name
                }
            else:
                return {
                    "success": True,
                    "found": False,
                    "company": None,
                    "agent": self.name
                }

        except Exception as e:
            return self.handle_error(e, context={"company_name": company_name})

    async def create_company(
        self,
        company_data: Dict[str, Any],
        check_existing: bool = True
    ) -> Dict[str, Any]:
        """
        Create a new company in HubSpot CRM.

        Args:
            company_data: Dictionary containing company information
            check_existing: If True, check if company exists before creating

        Returns:
            Dictionary with creation results
        """
        try:
            company_name = company_data.get("name")
            if not company_name:
                return {
                    "success": False,
                    "error": "Company name is required",
                    "agent": self.name
                }

            # Check if company already exists
            if check_existing:
                self.log_info(f"Checking if company exists: {company_name}")
                existing = await self.mcp.search_company(company_name)

                if existing:
                    self.log_info(f"Company already exists: {company_name}")
                    return {
                        "success": True,
                        "created": False,
                        "exists": True,
                        "company": existing,
                        "message": f"Company '{company_name}' already exists in HubSpot",
                        "agent": self.name
                    }

            # Create new company
            self.log_info(f"Creating new company: {company_name}")
            result = await self.mcp.create_company(company_data)

            if result:
                return {
                    "success": True,
                    "created": True,
                    "exists": False,
                    "company": result,
                    "message": f"Successfully created company '{company_name}' in HubSpot",
                    "agent": self.name
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to create company in HubSpot",
                    "agent": self.name
                }

        except Exception as e:
            return self.handle_error(e, context={"company_data": company_data})

    async def create_contact(
        self,
        contact_data: Dict[str, Any],
        company_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new contact in HubSpot CRM.

        Args:
            contact_data: Dictionary containing contact information
            company_id: Optional company ID to associate the contact with

        Returns:
            Dictionary with creation results
        """
        try:
            email = contact_data.get("email")
            if not email:
                return {
                    "success": False,
                    "error": "Contact email is required",
                    "agent": self.name
                }

            # Add company association if provided
            if company_id:
                contact_data["company_id"] = company_id

            self.log_info(f"Creating new contact: {email}")
            result = await self.mcp.create_contact(contact_data)

            if result:
                return {
                    "success": True,
                    "created": True,
                    "contact": result,
                    "message": f"Successfully created contact '{email}' in HubSpot",
                    "agent": self.name
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to create contact in HubSpot",
                    "agent": self.name
                }

        except Exception as e:
            return self.handle_error(e, context={"contact_data": contact_data})

    async def add_note(
        self,
        record_id: str,
        note_text: str,
        record_type: str = "company"
    ) -> Dict[str, Any]:
        """
        Add a note to a HubSpot record.

        Args:
            record_id: ID of the company or contact
            note_text: The note content
            record_type: Type of record ("company" or "contact")

        Returns:
            Dictionary with operation results
        """
        try:
            self.log_info(f"Adding note to {record_type}: {record_id}")

            success = await self.mcp.add_note(record_id, note_text, record_type)

            if success:
                return {
                    "success": True,
                    "message": f"Successfully added note to {record_type}",
                    "agent": self.name
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to add note to {record_type}",
                    "agent": self.name
                }

        except Exception as e:
            return self.handle_error(
                e,
                context={
                    "record_id": record_id,
                    "record_type": record_type,
                    "note_text": note_text[:100]
                }
            )

    async def create_company_with_contacts(
        self,
        company_data: Dict[str, Any],
        contacts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create a company and associated contacts in one operation.

        Args:
            company_data: Dictionary containing company information
            contacts: List of contact dictionaries

        Returns:
            Dictionary with operation results
        """
        try:
            company_name = company_data.get("name")
            self.log_info(f"Creating company with contacts: {company_name}")

            # Create company
            company_result = await self.create_company(company_data)

            if not company_result.get("success"):
                return company_result

            company_id = company_result.get("company", {}).get("id")
            created_contacts = []
            failed_contacts = []

            # Create contacts
            for contact_data in contacts:
                contact_result = await self.create_contact(contact_data, company_id)

                if contact_result.get("success"):
                    created_contacts.append(contact_result.get("contact"))
                else:
                    failed_contacts.append({
                        "contact": contact_data,
                        "error": contact_result.get("error")
                    })

            return {
                "success": True,
                "company": company_result.get("company"),
                "contacts_created": len(created_contacts),
                "contacts_failed": len(failed_contacts),
                "created_contacts": created_contacts,
                "failed_contacts": failed_contacts,
                "message": f"Created company and {len(created_contacts)} contacts in HubSpot",
                "agent": self.name
            }

        except Exception as e:
            return self.handle_error(
                e,
                context={
                    "company_data": company_data,
                    "contact_count": len(contacts)
                }
            )

    async def add_research_note(
        self,
        company_id: str,
        research_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add a formatted research note to a company record.

        Args:
            company_id: ID of the company
            research_data: Dictionary containing research findings

        Returns:
            Dictionary with operation results
        """
        try:
            # Format research data into a note
            note_lines = ["=== Company Research ==="]

            if "company_data" in research_data:
                company_info = research_data["company_data"]
                note_lines.append(f"\nIndustry: {company_info.get('industry', 'N/A')}")
                note_lines.append(f"Size: {company_info.get('size', 'N/A')} employees")
                note_lines.append(f"Funding: {company_info.get('funding', 'N/A')}")
                note_lines.append(f"Description: {company_info.get('description', 'N/A')}")

            if "icp_score" in research_data:
                note_lines.append(f"\n=== ICP Assessment ===")
                note_lines.append(f"Score: {research_data['icp_score']}/10")
                note_lines.append(f"Reasoning: {research_data.get('icp_reasoning', 'N/A')}")

            if "recent_news" in research_data:
                note_lines.append(f"\n=== Recent News ===")
                for news_item in research_data["recent_news"][:3]:
                    note_lines.append(f"- {news_item}")

            note_text = "\n".join(note_lines)

            return await self.add_note(company_id, note_text, record_type="company")

        except Exception as e:
            return self.handle_error(
                e,
                context={
                    "company_id": company_id,
                    "research_data_keys": list(research_data.keys())
                }
            )
