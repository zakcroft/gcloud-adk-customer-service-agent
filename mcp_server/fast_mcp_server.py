from fastmcp import FastMCP


mcp = FastMCP(name="customer-services-mcp-server")


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