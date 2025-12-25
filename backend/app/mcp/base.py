"""Base MCP integration class."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import yaml
from pathlib import Path


class BaseMCPIntegration(ABC):
    """Base class for MCP integrations."""

    name: str = "base"
    enabled: bool = False

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", False)

    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the external service."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection to the external service."""
        pass

    @abstractmethod
    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action on the external service."""
        pass

    @abstractmethod
    def get_available_actions(self) -> List[str]:
        """Get list of available actions."""
        pass


class MCPManager:
    """Manager for MCP integrations."""

    def __init__(self, config_path: Optional[str] = None):
        self.integrations: Dict[str, BaseMCPIntegration] = {}
        self.config = self._load_config(config_path)
        self._register_integrations()

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load MCP configuration."""
        if config_path:
            path = Path(config_path)
            if path.exists():
                with open(path) as f:
                    return yaml.safe_load(f)

        return {
            "integrations": {
                "database": {"enabled": True, "provider": "sqlite"},
                "calendar": {"enabled": False},
                "slack": {"enabled": False},
                "email": {"enabled": False},
            }
        }

    def _register_integrations(self) -> None:
        """Register available integrations."""
        from app.mcp.database import DatabaseMCP
        from app.mcp.calendar import CalendarMCP
        from app.mcp.slack import SlackMCP
        from app.mcp.email import EmailMCP

        integration_classes = {
            "database": DatabaseMCP,
            "calendar": CalendarMCP,
            "slack": SlackMCP,
            "email": EmailMCP,
        }

        for name, cls in integration_classes.items():
            config = self.config.get("integrations", {}).get(name, {})
            self.integrations[name] = cls(config)

    async def connect_all(self) -> None:
        """Connect all enabled integrations."""
        for name, integration in self.integrations.items():
            if integration.enabled:
                await integration.connect()

    async def disconnect_all(self) -> None:
        """Disconnect all integrations."""
        for integration in self.integrations.values():
            await integration.disconnect()

    def get_integration(self, name: str) -> Optional[BaseMCPIntegration]:
        """Get an integration by name."""
        return self.integrations.get(name)

    async def execute(self, integration_name: str, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action on an integration."""
        integration = self.get_integration(integration_name)
        if not integration:
            raise ValueError(f"Unknown integration: {integration_name}")
        if not integration.enabled:
            raise ValueError(f"Integration not enabled: {integration_name}")
        return await integration.execute(action, params)