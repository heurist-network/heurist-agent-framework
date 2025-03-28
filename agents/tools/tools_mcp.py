import json
import logging
from typing import Any, Dict, List, Optional

from clients.mcp_client import MCPClient

logger = logging.getLogger(__name__)


class Tools:
    def __init__(self, mcp_server_url="http://localhost:8000/sse"):
        self.mcp_url = mcp_server_url
        self.mcp_client = MCPClient()
        self.available_tools = []
        self.tools_config = []

    async def initialize(self, server_url: str = "http://localhost:8000/sse"):
        """Initialize the MCP client and fetch available tools"""
        try:
            print(f"Connecting to MCP server with URL: {self.mcp_url}")
            tools = await self.mcp_client.connect_to_sse_server(server_url=server_url)
            self.available_tools = tools
            self.tools_config = self.mcp_client.get_available_tools_json()
            logger.info(f"Connected to MCP server with {len(tools)} tools")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize MCP Client: {str(e)}")
            return False

    def get_tools_config(self, filter_tools: List[str] = None) -> List[Dict[str, Any]]:
        """
        Get tool configurations, optionally filtered by tool names

        Args:
            filter_tools: Optional list of tool names to include

        Returns:
            List of tool configurations
        """
        all_tools = self.tools_config

        if filter_tools:
            return [tool for tool in all_tools if tool["function"]["name"] in filter_tools]
        return all_tools

    async def execute_tool(self, tool_name: str, args: Dict[str, Any], agent_context: Any) -> Optional[Dict[str, Any]]:
        """Execute a tool by name with given arguments"""
        try:
            # Call the tool through MCP
            result = await self.mcp_client.call_tool(tool_name, args)
            if result:
                # Get the actual data structure instead of a formatted string
                formatted_content = self.mcp_client.format_result(result.content)

                # Format the response
                formatted_result = {"tool_name": tool_name, "args": args, "result": formatted_content}

                # Add the tool_call field for compatibility
                formatted_result["tool_call"] = json.dumps(
                    {"tool_call": tool_name, "processed": True, "args": args, "result": formatted_content},
                    default=str,
                )

                return formatted_result

        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return {
                "tool_name": tool_name,
                "args": args,
                "error": str(e),
                "tool_call": json.dumps(
                    {"tool_call": tool_name, "processed": False, "args": args, "error": str(e)},
                    default=str,
                ),
            }
