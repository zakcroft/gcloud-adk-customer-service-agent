"""
Query the MCP server to list available tools.
"""
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def query_tools():
    """Query the MCP server for available tools."""
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command=".venv/bin/python",
        args=["mcp_server/server.py"],
        env={**os.environ, "PYTHONPATH": "."},
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            
            print("=" * 80)
            print("MCP SERVER TOOLS")
            print("=" * 80)
            print(f"\nTotal tools available: {len(tools_result.tools)}\n")
            
            for i, tool in enumerate(tools_result.tools, 1):
                print(f"{i}. {tool.name}")
                print(f"   Description: {tool.description}")
                if hasattr(tool, 'inputSchema') and tool.inputSchema:
                    print(f"   Input Schema:")
                    if 'properties' in tool.inputSchema:
                        for prop_name, prop_details in tool.inputSchema['properties'].items():
                            prop_type = prop_details.get('type', 'unknown')
                            prop_desc = prop_details.get('description', 'No description')
                            required = prop_name in tool.inputSchema.get('required', [])
                            req_marker = " (required)" if required else " (optional)"
                            print(f"     - {prop_name}: {prop_type}{req_marker}")
                            print(f"       {prop_desc}")
                print()


if __name__ == "__main__":
    asyncio.run(query_tools())

