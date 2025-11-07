"""Base agent class for all agents."""
from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all agents with common functionality."""
    
    def __init__(self, name: str):
        """
        Initialize base agent.
        
        Args:
            name: Name of the agent (e.g., "Gmail Agent", "HubSpot Agent")
        """
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")
        self.logger.info(f"Initialized {name}")
    
    @abstractmethod
    async def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute the agent's main functionality.
        
        This method must be implemented by all subclasses.
        
        Returns:
            Dict containing execution results with at least:
            - success: bool indicating if execution succeeded
            - agent: str with agent name
        """
        pass
    
    def handle_error(self, error: Exception, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Common error handling for all agents.
        
        Args:
            error: The exception that occurred
            context: Optional context dictionary for logging
        
        Returns:
            Dict with error information
        """
        self.logger.error(
            f"Error in {self.name}: {str(error)}",
            exc_info=True,
            extra=context or {}
        )
        return {
            "success": False,
            "error": str(error),
            "error_type": type(error).__name__,
            "agent": self.name
        }
    
    def log_info(self, message: str, context: Optional[Dict] = None):
        """Log info message with agent context."""
        self.logger.info(f"{self.name}: {message}", extra=context or {})
    
    def log_warning(self, message: str, context: Optional[Dict] = None):
        """Log warning message with agent context."""
        self.logger.warning(f"{self.name}: {message}", extra=context or {})
    
    def log_error(self, message: str, context: Optional[Dict] = None):
        """Log error message with agent context."""
        self.logger.error(f"{self.name}: {message}", extra=context or {})
