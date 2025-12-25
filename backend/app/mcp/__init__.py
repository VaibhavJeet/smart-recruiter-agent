"""MCP (Model Context Protocol) integrations."""

from app.mcp.base import BaseMCPIntegration, MCPManager
from app.mcp.database import DatabaseMCP
from app.mcp.calendar import CalendarMCP
from app.mcp.slack import SlackMCP
from app.mcp.email import EmailMCP

__all__ = [
    "BaseMCPIntegration",
    "MCPManager",
    "DatabaseMCP",
    "CalendarMCP",
    "SlackMCP",
    "EmailMCP",
]