import asyncio

import json

from mcp import types as mcp_types
from mcp.server import NotificationOptions
from mcp.server.lowlevel import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio

from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

from app.agent.tools.tools import (
    check_product_list as ft_check_product_list,
    get_product_recommendations as ft_get_product_recommendations,
    check_product_availability as ft_check_product_availability,
    access_cart_information as ft_access_cart_information,
    modify_cart as ft_modify_cart,
)


def create_mcp_server():
    check_product_list = FunctionTool(ft_check_product_list)
    get_product_recommendations = FunctionTool(ft_get_product_recommendations)
    check_product_availability = FunctionTool(ft_check_product_availability)
    access_cart_information = FunctionTool(ft_access_cart_information)
    modify_cart = FunctionTool(ft_modify_cart)

    app = Server("customer-services-mcp-server")

    @app.list_tools()
    async def list_tools() -> list[mcp_types.Tool]:
        mcp_tools = [
            adk_to_mcp_tool_type(check_product_list),
            adk_to_mcp_tool_type(get_product_recommendations),
            adk_to_mcp_tool_type(check_product_availability),
            adk_to_mcp_tool_type(access_cart_information),
            adk_to_mcp_tool_type(modify_cart),
        ]
        return mcp_tools

    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[mcp_types.TextContent]:
        tools = {
            check_product_list.name: check_product_list,
            get_product_recommendations.name: get_product_recommendations,
            check_product_availability.name: check_product_availability,
            access_cart_information.name: access_cart_information,
            modify_cart.name: modify_cart,
        }

        if name in tools:
            try:
                result = await tools[name].run_async(
                    args=arguments,
                    tool_context=None,
                )
                print("result", result)
                return [mcp_types.TextContent(type="text", text=json.dumps(result))]
            except Exception as e:
                return [
                    mcp_types.TextContent(
                        type="text", text=json.dumps({"error": str(e)})
                    )
                ]
        else:
            return [
                mcp_types.TextContent(
                    type="text", text=json.dumps({"error": f"Tool '{name}' not found"})
                )
            ]

    return app


async def run_mcp_server():
    app = create_mcp_server()

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        print("MCP Stdio Server: Starting handshake with client...")
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,  # Use the server name defined above
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    # Define server capabilities - consult MCP docs for options
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
        print("MCP Stdio Server: Run loop finished or client disconnected.")

if __name__ == "__main__":
    print("Launching MCP Server to expose ADK tools via stdio...")
    try:
        asyncio.run(run_mcp_server())
    except KeyboardInterrupt:
        print("\nMCP Server (stdio) stopped by user.")
    except Exception as e:
        print(f"MCP Server (stdio) encountered an error: {e}")
    finally:
        print("MCP Server (stdio) process exiting.")


