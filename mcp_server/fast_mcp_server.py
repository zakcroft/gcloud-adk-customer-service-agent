from fastmcp import FastMCP

# Import and register your existing tools directly
from app.agent.tools.tools import (
    check_product_list,
    get_product_recommendations,
    check_product_availability,
    access_cart_information,
    modify_cart,
)


mcp = FastMCP(name="customer-services-mcp-server")


# ============================================================================
# TOOLS - Register existing functions as MCP tools
# ============================================================================

mcp.tool(check_product_list)
mcp.tool(get_product_recommendations)
mcp.tool(check_product_availability)
mcp.tool(access_cart_information)
mcp.tool(modify_cart)


# ============================================================================
# RESOURCES - Configuration and Data
# ============================================================================

# Static resource
@mcp.resource("config://version")
def get_version():
    return "2.0.1"


# Dynamic resource template
@mcp.resource("users://{user_id}/profile")
def get_profile(user_id: int):
    # Fetch profile for user_id...
    return {"name": f"User {user_id}", "status": "active"}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")