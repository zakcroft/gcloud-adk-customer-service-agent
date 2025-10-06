from fastmcp import FastMCP, Client

mcp = FastMCP("My MCP Server")

async def main():
    # Connect via in-memory transport
    async with Client(mcp) as client:
            print(await client.call_tool("config://version", {}))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

