"""Email MCP integration."""

from typing import Dict, Any, List
from app.mcp.base import BaseMCPIntegration


class EmailMCP(BaseMCPIntegration):
    """Email integration via MCP (SMTP, Gmail API)."""

    name = "email"

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.provider = config.get("provider", "smtp")
        self.host = config.get("host")
        self.port = config.get("port", 587)
        self.username = config.get("username")
        self.password = config.get("password")
        self.client = None

    async def connect(self) -> bool:
        if not self.enabled:
            return False
        return True

    async def disconnect(self) -> None:
        self.client = None

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        actions = {
            "send": self._send_email,
            "send_template": self._send_template,
        }
        if action not in actions:
            raise ValueError(f"Unknown action: {action}")
        return await actions[action](params)

    def get_available_actions(self) -> List[str]:
        return ["send", "send_template"]

    async def _send_email(self, params: Dict[str, Any]) -> Dict[str, Any]:
        to = params.get("to")
        return {"status": "success", "message_id": "msg_123", "to": to}

    async def _send_template(self, params: Dict[str, Any]) -> Dict[str, Any]:
        template_name = params.get("template")
        to = params.get("to")
        return {"status": "success", "message_id": "msg_123", "template": template_name, "to": to}