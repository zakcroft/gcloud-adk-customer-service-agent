

import asyncio
import json
from typing import Optional, Any, Dict, List
from fastmcp import FastMCP, Client


class CustomerServicesMCPClient:

    def __init__(self, server: FastMCP):
        """
        Initialize the MCP client.

        Args:
            server: The FastMCP server instance to connect to
        """
        self.server = server
        self.client: Optional[Client] = None
        
    async def __aenter__(self):
        """Async context manager entry."""
        self.client = Client(self.server)
        await self.client.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)
    
    # ============================================================================
    # TOOL DISCOVERY
    # ============================================================================
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all available tools on the server.
        
        Returns:
            List of tool definitions with names, descriptions, and parameters
        """
        if not self.client:
            raise RuntimeError("Client not connected. Use 'async with' context manager.")
        
        tools = await self.client.list_tools()
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
            for tool in tools
        ]
    
    async def print_available_tools(self):
        """Print all available tools in a readable format."""
        tools = await self.list_tools()
        print("\n" + "="*80)
        print("AVAILABLE TOOLS")
        print("="*80)
        for tool in tools:
            print(f"\n📦 {tool['name']}")
            print(f"   {tool['description']}")
            if 'properties' in tool['input_schema']:
                print("   Parameters:")
                for param_name, param_info in tool['input_schema']['properties'].items():
                    required = param_name in tool['input_schema'].get('required', [])
                    req_marker = "* " if required else "  "
                    param_type = param_info.get('type', 'any')
                    param_desc = param_info.get('description', 'No description')
                    print(f"     {req_marker}{param_name} ({param_type}): {param_desc}")
        print("\n" + "="*80 + "\n")
    
    # ============================================================================
    # PRODUCT TOOLS
    # ============================================================================
    
    async def check_product_list(self, department: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a list of products by department or all products.
        
        Args:
            department: Optional department filter (tools, seeds, decor, irrigation)
            
        Returns:
            Dictionary with products list and metadata
        """
        if not self.client:
            raise RuntimeError("Client not connected. Use 'async with' context manager.")
        
        args = {}
        if department is not None:
            args["department"] = department
            
        result = await self.client.call_tool("check_product_list", args)
        return self._parse_result(result)
    
    async def get_product_recommendations(
        self, 
        plant_type: str, 
        customer_id: str
    ) -> Dict[str, Any]:
        """
        Get product recommendations based on plant type and customer profile.
        
        Args:
            plant_type: The type of plant (e.g., 'Petunias', 'Tomatoes', 'Sunflowers')
            customer_id: Customer ID for personalized recommendations
            
        Returns:
            Dictionary of recommended products with pricing and availability
        """
        if not self.client:
            raise RuntimeError("Client not connected. Use 'async with' context manager.")
        
        result = await self.client.call_tool(
            "get_product_recommendations",
            {
                "plant_type": plant_type,
                "customer_id": customer_id
            }
        )
        return self._parse_result(result)
    
    async def check_product_availability(
        self, 
        product_id: str, 
        store_id: str
    ) -> Dict[str, Any]:
        """
        Check the availability of a product at a specified store.
        
        Args:
            product_id: The ID of the product to check
            store_id: The ID of the store or 'pickup' for pickup availability
            
        Returns:
            Dictionary indicating availability with detailed stock information
        """
        if not self.client:
            raise RuntimeError("Client not connected. Use 'async with' context manager.")
        
        result = await self.client.call_tool(
            "check_product_availability",
            {
                "product_id": product_id,
                "store_id": store_id
            }
        )
        return self._parse_result(result)
    
    # ============================================================================
    # CART TOOLS
    # ============================================================================
    
    async def access_cart_information(self, customer_id: str) -> Dict[str, Any]:
        """
        Retrieve the current cart contents for a customer.
        
        Args:
            customer_id: The ID of the customer
            
        Returns:
            Dictionary representing the cart contents with detailed pricing
        """
        if not self.client:
            raise RuntimeError("Client not connected. Use 'async with' context manager.")
        
        result = await self.client.call_tool(
            "access_cart_information",
            {"customer_id": customer_id}
        )
        return self._parse_result(result)
    
    async def modify_cart(
        self,
        customer_id: str,
        items_to_add: Optional[List[Dict[str, Any]]] = None,
        items_to_remove: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Modify the user's shopping cart by adding and/or removing items.
        
        Args:
            customer_id: The ID of the customer
            items_to_add: List of dicts with 'product_id' and 'quantity' keys
            items_to_remove: List of dicts with 'product_id' and 'quantity' keys
            
        Returns:
            Detailed status of the cart modification with updated totals
        """
        if not self.client:
            raise RuntimeError("Client not connected. Use 'async with' context manager.")
        
        result = await self.client.call_tool(
            "modify_cart",
            {
                "customer_id": customer_id,
                "items_to_add": items_to_add or [],
                "items_to_remove": items_to_remove or []
            }
        )
        return self._parse_result(result)
    
    # ============================================================================
    # RESOURCE ACCESS
    # ============================================================================
    
    async def get_version(self) -> str:
        """
        Get the server version.
        
        Returns:
            Version string
        """
        if not self.client:
            raise RuntimeError("Client not connected. Use 'async with' context manager.")
        
        result = await self.client.read_resource("config://version")
        
        # Parse resource result
        if isinstance(result, list) and len(result) > 0:
            first_item = result[0]
            if hasattr(first_item, 'text'):
                return first_item.text
        
        return str(result)
    
    async def get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """
        Get a user profile by ID.
        
        Args:
            user_id: The user ID
            
        Returns:
            User profile dictionary
        """
        if not self.client:
            raise RuntimeError("Client not connected. Use 'async with' context manager.")
        
        result = await self.client.read_resource(f"users://{user_id}/profile")
        
        # Parse resource result
        if isinstance(result, list) and len(result) > 0:
            first_item = result[0]
            if hasattr(first_item, 'text'):
                try:
                    return json.loads(first_item.text)
                except json.JSONDecodeError:
                    return {"raw_result": first_item.text}
        
        return result
    
    # ============================================================================
    # UTILITY METHODS
    # ============================================================================
    
    def _parse_result(self, result: Any) -> Dict[str, Any]:
        """
        Parse the result from a tool call.
        
        Args:
            result: Raw result from tool call
            
        Returns:
            Parsed dictionary result
        """
        # Handle CallToolResult objects
        if hasattr(result, 'content'):
            content = result.content
            if isinstance(content, list) and len(content) > 0:
                first_item = content[0]
                if hasattr(first_item, 'text'):
                    try:
                        return json.loads(first_item.text)
                    except json.JSONDecodeError:
                        return {"raw_result": first_item.text}
        
        # Handle string results
        if isinstance(result, str):
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"raw_result": result}
        
        # Handle list of TextContent objects
        elif isinstance(result, list) and len(result) > 0:
            first_item = result[0]
            if hasattr(first_item, 'text'):
                try:
                    return json.loads(first_item.text)
                except json.JSONDecodeError:
                    return {"raw_result": first_item.text}
        
        return result
    
    @staticmethod
    def pretty_print(data: Any, title: Optional[str] = None):
        """
        Pretty print data with optional title.
        
        Args:
            data: Data to print
            title: Optional title to display
        """
        if title:
            print("\n" + "="*80)
            print(f"  {title}")
            print("="*80)
        
        print(json.dumps(data, indent=2, default=str))
        print()


# ============================================================================
# EXAMPLE USAGE AND DEMONSTRATIONS
# ============================================================================

async def demo_all_features():
    """Comprehensive demonstration of all client features."""
    
    # Import the server
    from fast_mcp_server import mcp
    
    print("\n" + "🚀 "*20)
    print("CUSTOMER SERVICES MCP CLIENT - FULL DEMONSTRATION")
    print("🚀 "*20 + "\n")
    
    async with CustomerServicesMCPClient(mcp) as client:
        
        # 1. List all available tools
        print("\n📋 STEP 1: Discovering Available Tools")
        await client.print_available_tools()
        
        # 2. Check product list - all products
        print("\n🛍️  STEP 2: Checking All Products")
        all_products = await client.check_product_list()
        client.pretty_print(all_products, "All Products")
        
        # 3. Check product list - specific department
        print("\n🌱 STEP 3: Checking Seeds Department")
        seeds = await client.check_product_list(department="seeds")
        client.pretty_print(seeds, "Seeds Department Products")
        
        # 4. Get product recommendations
        print("\n💡 STEP 4: Getting Product Recommendations for Tomatoes")
        recommendations = await client.get_product_recommendations(
            plant_type="Tomatoes",
            customer_id="CUST-12345"
        )
        client.pretty_print(recommendations, "Tomato Growing Recommendations")
        
        # 5. Check product availability
        print("\n📦 STEP 5: Checking Product Availability")
        availability = await client.check_product_availability(
            product_id="seed-101",
            store_id="STORE-001"
        )
        client.pretty_print(availability, "Product Availability")
        
        # 6. Access cart information
        print("\n🛒 STEP 6: Accessing Cart Information")
        cart = await client.access_cart_information(customer_id="CUST-12345")
        client.pretty_print(cart, "Customer Cart")
        
        # 7. Modify cart - add items
        print("\n➕ STEP 7: Adding Items to Cart")
        modified_cart = await client.modify_cart(
            customer_id="CUST-12345",
            items_to_add=[
                {"product_id": "tool-001", "quantity": 1},
                {"product_id": "seed-102", "quantity": 3}
            ]
        )
        client.pretty_print(modified_cart, "Cart After Adding Items")
        
        # 8. Modify cart - remove items
        print("\n➖ STEP 8: Removing Items from Cart")
        modified_cart = await client.modify_cart(
            customer_id="CUST-12345",
            items_to_remove=[
                {"product_id": "soil-123", "quantity": 1}
            ]
        )
        client.pretty_print(modified_cart, "Cart After Removing Items")
        
        # 9. Access resources
        print("\n🔧 STEP 9: Accessing Server Resources")
        version = await client.get_version()
        print(f"Server Version: {version}")
        
        user_profile = await client.get_user_profile(user_id=42)
        client.pretty_print(user_profile, "User Profile")
        
        print("\n" + "✅ "*20)
        print("DEMONSTRATION COMPLETE!")
        print("✅ "*20 + "\n")


async def quick_example():
    """Quick example showing basic usage."""
    from fast_mcp_server import mcp
    
    print("\n🚀 Quick Example: Checking Products and Cart\n")
    
    async with CustomerServicesMCPClient(mcp) as client:
        # Get all products
        products = await client.check_product_list()
        print(f"Total products available: {products['total_products']}")
        
        # Get recommendations
        recs = await client.get_product_recommendations(
            plant_type="Petunias",
            customer_id="CUST-001"
        )
        print(f"Recommendations for Petunias: {recs['total_recommendations']} items")
        
        # Check cart
        cart = await client.access_cart_information(customer_id="CUST-001")
        print(f"Cart total: £{cart['total']} ({cart['item_count']} items)")


async def main():
    """Main entry point - choose which demo to run."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        await quick_example()
    else:
        await demo_all_features()


if __name__ == "__main__":
    asyncio.run(main())