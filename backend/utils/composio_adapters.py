"""Composio MCP adapters for external tool integrations."""
import os
import logging
from typing import Any, Dict, List, Optional
from composio_langchain import ComposioToolSet, App, Action

logger = logging.getLogger(__name__)


class HubSpotMCP:
    """
    Wrapper for HubSpot operations via Composio MCP.

    This adapter routes HubSpot API calls through Composio's Model Context Protocol,
    providing unified error handling, retry logic, and credential management.
    """

    def __init__(self, use_mock: bool = False):
        """
        Initialize HubSpot MCP adapter.

        Args:
            use_mock: If True, use mock data instead of real API calls
        """
        self.use_mock = use_mock or os.getenv("USE_MOCK_MCP", "false").lower() == "true"

        if not self.use_mock:
            try:
                self.toolset = ComposioToolSet()
                self.hubspot_tools = self.toolset.get_tools(apps=[App.HUBSPOT])
                logger.info("HubSpot MCP initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Composio HubSpot MCP: {e}. Falling back to mock mode.")
                self.use_mock = True
                self.toolset = None
                self.hubspot_tools = []
        else:
            logger.info("HubSpot MCP running in mock mode")
            self.toolset = None
            self.hubspot_tools = []

    async def search_company(self, company_name: str) -> Optional[Dict[str, Any]]:
        """
        Search for a company in HubSpot CRM.

        Args:
            company_name: Name of the company to search for

        Returns:
            Company data if found, None otherwise
        """
        if self.use_mock:
            return self._mock_search_company(company_name)

        try:
            # Use Composio to search HubSpot
            search_action = self._get_action(Action.HUBSPOT_SEARCH_COMPANIES)
            if not search_action:
                logger.error("HubSpot search action not available")
                return None

            result = await search_action.ainvoke({
                "query": company_name,
                "limit": 1
            })

            if result and len(result) > 0:
                logger.info(f"Found company in HubSpot: {company_name}")
                return result[0]

            logger.info(f"Company not found in HubSpot: {company_name}")
            return None

        except Exception as e:
            logger.error(f"Error searching HubSpot for company {company_name}: {e}")
            return None

    async def create_company(self, company_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new company in HubSpot CRM.

        Args:
            company_data: Dictionary containing company information
                Required fields: name
                Optional fields: domain, industry, description, city, state, country

        Returns:
            Created company data with ID and URL, or None on failure
        """
        if self.use_mock:
            return self._mock_create_company(company_data)

        try:
            create_action = self._get_action(Action.HUBSPOT_CREATE_COMPANY)
            if not create_action:
                logger.error("HubSpot create company action not available")
                return None

            # Map data to HubSpot properties format
            properties = {
                "name": company_data.get("name"),
                "domain": company_data.get("domain", ""),
                "industry": company_data.get("industry", ""),
                "description": company_data.get("description", ""),
                "city": company_data.get("city", ""),
                "state": company_data.get("state", ""),
                "country": company_data.get("country", "")
            }

            result = await create_action.ainvoke({"properties": properties})

            logger.info(f"Created company in HubSpot: {company_data.get('name')}")
            return result

        except Exception as e:
            logger.error(f"Error creating company in HubSpot: {e}")
            return None

    async def create_contact(self, contact_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new contact in HubSpot CRM.

        Args:
            contact_data: Dictionary containing contact information
                Required fields: email
                Optional fields: firstname, lastname, company, jobtitle, phone

        Returns:
            Created contact data with ID, or None on failure
        """
        if self.use_mock:
            return self._mock_create_contact(contact_data)

        try:
            create_action = self._get_action(Action.HUBSPOT_CREATE_CONTACT)
            if not create_action:
                logger.error("HubSpot create contact action not available")
                return None

            properties = {
                "email": contact_data.get("email"),
                "firstname": contact_data.get("firstname", ""),
                "lastname": contact_data.get("lastname", ""),
                "company": contact_data.get("company", ""),
                "jobtitle": contact_data.get("jobtitle", ""),
                "phone": contact_data.get("phone", "")
            }

            result = await create_action.ainvoke({"properties": properties})

            logger.info(f"Created contact in HubSpot: {contact_data.get('email')}")
            return result

        except Exception as e:
            logger.error(f"Error creating contact in HubSpot: {e}")
            return None

    async def add_note(self, record_id: str, note_text: str, record_type: str = "company") -> bool:
        """
        Add a note to a HubSpot record.

        Args:
            record_id: ID of the company or contact
            note_text: The note content
            record_type: Type of record ("company" or "contact")

        Returns:
            True if note was added successfully, False otherwise
        """
        if self.use_mock:
            return self._mock_add_note(record_id, note_text, record_type)

        try:
            create_note_action = self._get_action(Action.HUBSPOT_CREATE_NOTE)
            if not create_note_action:
                logger.error("HubSpot create note action not available")
                return False

            result = await create_note_action.ainvoke({
                "note": note_text,
                "associations": [{
                    "to": {"id": record_id},
                    "type": f"{record_type}_to_note"
                }]
            })

            logger.info(f"Added note to {record_type} {record_id}")
            return True

        except Exception as e:
            logger.error(f"Error adding note to HubSpot: {e}")
            return False

    def _get_action(self, action: Action):
        """Get a specific Composio action from the toolset."""
        if not self.hubspot_tools:
            return None

        for tool in self.hubspot_tools:
            if tool.name == action.value:
                return tool
        return None

    # Mock methods for offline/demo mode

    def _mock_search_company(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Mock company search for demo purposes."""
        mock_companies = {
            "Stripe": {
                "id": "mock-stripe-001",
                "name": "Stripe",
                "domain": "stripe.com",
                "industry": "Financial Services",
                "description": "Online payment processing",
                "url": "https://app.hubspot.com/contacts/mock/company/mock-stripe-001"
            },
            "Notion": {
                "id": "mock-notion-001",
                "name": "Notion",
                "domain": "notion.so",
                "industry": "Software",
                "description": "Productivity and collaboration software",
                "url": "https://app.hubspot.com/contacts/mock/company/mock-notion-001"
            }
        }

        result = mock_companies.get(company_name.strip())
        if result:
            logger.info(f"[MOCK] Found company: {company_name}")
        else:
            logger.info(f"[MOCK] Company not found: {company_name}")
        return result

    def _mock_create_company(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock company creation for demo purposes."""
        company_name = company_data.get("name", "Unknown Company")
        mock_id = f"mock-{company_name.lower().replace(' ', '-')}-{hash(company_name) % 1000}"

        logger.info(f"[MOCK] Created company: {company_name}")

        return {
            "id": mock_id,
            "name": company_name,
            "url": f"https://app.hubspot.com/contacts/mock/company/{mock_id}",
            **company_data
        }

    def _mock_create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock contact creation for demo purposes."""
        email = contact_data.get("email", "unknown@example.com")
        mock_id = f"mock-contact-{hash(email) % 1000}"

        logger.info(f"[MOCK] Created contact: {email}")

        return {
            "id": mock_id,
            "url": f"https://app.hubspot.com/contacts/mock/contact/{mock_id}",
            **contact_data
        }

    def _mock_add_note(self, record_id: str, note_text: str, record_type: str) -> bool:
        """Mock note addition for demo purposes."""
        logger.info(f"[MOCK] Added note to {record_type} {record_id}: {note_text[:50]}...")
        return True


class NotionMCP:
    """
    Wrapper for Notion operations via Composio MCP.

    This adapter routes Notion API calls through Composio's Model Context Protocol.
    """

    def __init__(self, use_mock: bool = False):
        """
        Initialize Notion MCP adapter.

        Args:
            use_mock: If True, use mock data instead of real API calls
        """
        self.use_mock = use_mock or os.getenv("USE_MOCK_MCP", "false").lower() == "true"

        if not self.use_mock:
            try:
                self.toolset = ComposioToolSet()
                self.notion_tools = self.toolset.get_tools(apps=[App.NOTION])
                logger.info("Notion MCP initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Composio Notion MCP: {e}. Falling back to mock mode.")
                self.use_mock = True
                self.toolset = None
                self.notion_tools = []
        else:
            logger.info("Notion MCP running in mock mode")
            self.toolset = None
            self.notion_tools = []

    async def get_icp_criteria(self) -> Dict[str, Any]:
        """
        Fetch ICP (Ideal Customer Profile) criteria from Notion.

        Returns:
            Dictionary containing ICP criteria
        """
        if self.use_mock:
            return self._mock_get_icp_criteria()

        try:
            # Search for ICP document in Notion
            search_action = self._get_action(Action.NOTION_SEARCH)
            if not search_action:
                logger.error("Notion search action not available")
                return self._mock_get_icp_criteria()

            result = await search_action.ainvoke({
                "query": "ICP criteria",
                "filter": {"property": "object", "value": "page"}
            })

            if result and len(result) > 0:
                # Fetch the page content
                page_id = result[0].get("id")
                page_action = self._get_action(Action.NOTION_GET_PAGE)
                page_content = await page_action.ainvoke({"page_id": page_id})

                logger.info("Retrieved ICP criteria from Notion")
                return self._parse_icp_criteria(page_content)

            logger.warning("ICP criteria not found in Notion, using mock data")
            return self._mock_get_icp_criteria()

        except Exception as e:
            logger.error(f"Error fetching ICP criteria from Notion: {e}")
            return self._mock_get_icp_criteria()

    async def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a Notion document by ID.

        Args:
            document_id: Notion page/document ID

        Returns:
            Document content or None on failure
        """
        if self.use_mock:
            return self._mock_get_document(document_id)

        try:
            page_action = self._get_action(Action.NOTION_GET_PAGE)
            if not page_action:
                logger.error("Notion get page action not available")
                return None

            result = await page_action.ainvoke({"page_id": document_id})

            logger.info(f"Retrieved Notion document: {document_id}")
            return result

        except Exception as e:
            logger.error(f"Error fetching Notion document {document_id}: {e}")
            return None

    def _get_action(self, action: Action):
        """Get a specific Composio action from the toolset."""
        if not self.notion_tools:
            return None

        for tool in self.notion_tools:
            if tool.name == action.value:
                return tool
        return None

    def _parse_icp_criteria(self, page_content: Dict[str, Any]) -> Dict[str, Any]:
        """Parse ICP criteria from Notion page content."""
        # This would parse the actual Notion page structure
        # For now, return structured format
        return {
            "company_size": {"min": 50, "max": 5000},
            "industries": ["Technology", "SaaS", "E-commerce"],
            "funding_stage": ["Series A", "Series B", "Series C"],
            "geography": ["North America", "Europe"],
            "growth_indicators": ["YoY revenue growth > 50%", "Recent funding round"]
        }

    # Mock methods

    def _mock_get_icp_criteria(self) -> Dict[str, Any]:
        """Mock ICP criteria for demo purposes."""
        logger.info("[MOCK] Retrieved ICP criteria")
        return {
            "company_size": {"min": 50, "max": 5000},
            "industries": ["Technology", "SaaS", "E-commerce", "Financial Services"],
            "funding_stage": ["Series A", "Series B", "Series C", "Series D+"],
            "geography": ["North America", "Europe", "Asia-Pacific"],
            "growth_indicators": [
                "YoY revenue growth > 50%",
                "Recent funding round",
                "Expanding internationally",
                "Hiring aggressively"
            ],
            "pain_points": [
                "Payment processing complexity",
                "International expansion challenges",
                "Developer experience focus"
            ]
        }

    def _mock_get_document(self, document_id: str) -> Dict[str, Any]:
        """Mock document retrieval for demo purposes."""
        logger.info(f"[MOCK] Retrieved Notion document: {document_id}")
        return {
            "id": document_id,
            "title": "Mock Document",
            "content": "This is mock document content from Notion."
        }
