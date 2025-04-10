import asyncio
import json
import sys
from contextlib import AsyncExitStack
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client

load_dotenv()  # load environment variables from .env


class MCPClient:
    """Client for interacting with MCP (Model Context Protocol) servers"""

    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        # Initialize context attributes
        self._session_context = None
        self._streams_context = None
        # Store available tools
        self.available_tools = []

    async def connect_to_sse_server(self, server_url: str):
        """Connect to an MCP server running with SSE transport"""
        # Store the context managers so they stay alive
        self._streams_context = sse_client(url=server_url)
        streams = await self._streams_context.__aenter__()

        self._session_context = ClientSession(*streams)
        self.session: ClientSession = await self._session_context.__aenter__()

        # Initialize
        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        self.available_tools = response.tools

        return self.available_tools

    async def cleanup(self):
        """Properly clean up the session and streams"""
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)

    async def call_tool(self, tool_name: str, parameters: Dict[str, Any] = None):
        """Call a specific tool by name with the given parameters"""
        if not self.session:
            raise RuntimeError("MCP session not initialized. Call connect_to_sse_server first.")

        if not parameters:
            parameters = {}

        try:
            result = await self.session.call_tool(tool_name, parameters)
            return result
        except Exception as e:
            print(f"Error calling tool {tool_name}: {str(e)}")
            return None

    def get_tool_by_name(self, tool_name: str):
        """Get a tool by its name"""
        for tool in self.available_tools:
            if tool.name == tool_name:
                return tool
        return None

    def get_tools_by_category(self, category: str):
        """Get all tools that match a category (substring in name)"""
        return [tool for tool in self.available_tools if category.lower() in tool.name.lower()]

    def print_available_tools(self):
        """Print all available tools with their descriptions and input schemas"""
        if not self.available_tools:
            print("No tools available. Connect to a server first.")
            return
        print("Available tools:")
        print(self.available_tools)

        print(f"\nAvailable Tools ({len(self.available_tools)}):")
        for i, tool in enumerate(self.available_tools):
            print(f"{i + 1}. {tool.name}: {tool.description}")
            print(f"   Input schema: {tool.inputSchema}")
            print()

    def get_available_tools_json(self):
        """Return all available tools formatted for LLM consumption"""
        if not self.available_tools:
            return {"error": "No tools available. Connect to a server first."}

        tools_list = []

        for tool in self.available_tools:
            # Format each tool in a structure optimized for LLM consumption
            tool_data = {
                "type": "function",
                "function": {"name": tool.name, "description": tool.description, "parameters": tool.inputSchema},
            }
            tools_list.append(tool_data)

        return tools_list

    def format_result(self, content):
        """Format the result content for display and extract the actual JSON data"""
        try:
            # Handle the case where content is a list of TextContent objects
            if hasattr(content, "__iter__") and not isinstance(content, (str, dict)):
                # Extract the first TextContent object if it exists
                if content and hasattr(content[0], "text"):
                    text_content = content[0].text

                    # If the text content looks like a dictionary with single quotes, convert to proper JSON
                    if (
                        isinstance(text_content, str)
                        and text_content.strip().startswith("{")
                        and text_content.strip().endswith("}")
                    ):
                        # Replace single quotes with double quotes for JSON parsing
                        # This is a simple approach and might not work for all cases with nested quotes
                        try:
                            # First try to parse it directly
                            return json.loads(text_content)
                        except json.JSONDecodeError:
                            # If that fails, try to convert Python literal to proper JSON
                            import ast

                            python_dict = ast.literal_eval(text_content)
                            return python_dict
                    else:
                        return text_content

                # If it's an iterable but not TextContent objects, return as is
                return content

            # If content is a string that looks like JSON or Python dict
            elif isinstance(content, str) and content.strip().startswith("{") and content.strip().endswith("}"):
                try:
                    # First try to parse it as JSON
                    return json.loads(content)
                except json.JSONDecodeError:
                    # If that fails, try to convert Python literal to proper JSON
                    import ast

                    python_dict = ast.literal_eval(content)
                    return python_dict

            # If content is already a dict or list, return it directly
            elif isinstance(content, (dict, list)):
                return content

            # For other types, return as is
            else:
                return content

        except Exception as e:
            # If parsing fails, log the error and return the raw content
            print(f"Error formatting result: {str(e)}")
            return content


async def main():
    if len(sys.argv) < 2:
        print("Usage: python mcp_client.py <URL of SSE MCP server (i.e. http://localhost:8000/sse)>")
        sys.exit(1)

    client = MCPClient()
    try:
        # Connect to the MCP server
        print(f"Connecting to MCP server at {sys.argv[1]}...")
        tools = await client.connect_to_sse_server(server_url=sys.argv[1])
        print(f"Connected successfully! Found {len(tools)} available tools.")

        # Print available tools
        client.print_available_tools()

        # Simple demonstration - find and call a tool if available
        coingecko_tools = client.get_tools_by_category("coingecko")
        if coingecko_tools:
            tool = coingecko_tools[0]
            print(f"\nDemonstrating tool call with: {tool.name}")

            # Determine parameters based on tool schema
            params = {}
            if "token_name" in str(tool.inputSchema):
                params = {"token_name": "bitcoin"}
            elif "coingecko_id" in str(tool.inputSchema):
                params = {"coingecko_id": "bitcoin"}

            print(f"Calling with parameters: {params}")
            result = await client.call_tool(tool.name, params)
            if result:
                print("\nResult:")
                formatted_result = client.format_result(result.content)
                print(formatted_result)
        else:
            print("\nNo CoinGecko tools found for demonstration.")

        print("\nClient demonstration complete. Use main_mcp.py for the full agent integration.")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
