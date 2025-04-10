import asyncio
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from core.clients.mcp_client import MCPClient  # noqa: E402


async def main():
    if len(sys.argv) < 2:
        print("Usage: python test_mcp_client.py <server_url>")
        sys.exit(1)

    server_url = sys.argv[1]
    client = MCPClient()

    try:
        print(f"Connecting to MCP server at {server_url}...")
        await client.connect_to_sse_server(server_url)

        # Print all available tools
        client.print_available_tools()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
