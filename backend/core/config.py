"""Configuration and environment variables."""
import os
from typing import Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


class Config:
    """Application configuration."""

    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # WebSocket Configuration
    WS_HEARTBEAT_INTERVAL: int = int(os.getenv("WS_HEARTBEAT_INTERVAL", "30"))

    # Composio Configuration
    COMPOSIO_API_KEY: str = os.getenv("COMPOSIO_API_KEY", "")
    USE_COMPOSIO: bool = os.getenv("USE_COMPOSIO", "false").lower() == "true"
    USE_MOCK_MCP: bool = os.getenv("USE_MOCK_MCP", "false").lower() == "true"

    # HubSpot Configuration (for fallback direct API)
    HUBSPOT_API_KEY: str = os.getenv("HUBSPOT_API_KEY", "")

    # Notion Configuration (for fallback direct API)
    NOTION_API_KEY: str = os.getenv("NOTION_API_KEY", "")
    
    @classmethod
    def get_llm(cls) -> ChatOpenAI:
        """Get configured LangChain ChatOpenAI instance."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in environment variables")
        
        return ChatOpenAI(
            model=cls.OPENAI_MODEL,
            temperature=cls.OPENAI_TEMPERATURE,
            api_key=cls.OPENAI_API_KEY
        )
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY:
            return False
        return True

    @classmethod
    def get_composio_client(cls):
        """
        Get configured Composio client.

        Returns:
            ComposioToolSet instance or None if not configured
        """
        if not cls.USE_COMPOSIO:
            return None

        if not cls.COMPOSIO_API_KEY and not cls.USE_MOCK_MCP:
            raise ValueError("COMPOSIO_API_KEY not set in environment variables")

        try:
            from composio_langchain import ComposioToolSet
            return ComposioToolSet(api_key=cls.COMPOSIO_API_KEY if cls.COMPOSIO_API_KEY else None)
        except ImportError:
            raise ImportError("composio-langchain package not installed. Run: pip install composio-langchain")
