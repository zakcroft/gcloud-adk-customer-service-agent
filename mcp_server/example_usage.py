import asyncio
from fast_mcp_client import CustomerServicesMCPClient
from fast_mcp_server import mcp


async def example_1_browse_products():
    print("\n" + "="*80)
    print("EXAMPLE 1: Browse Products by Department")
    print("="*80)
    
    async with CustomerServicesMCPClient(mcp) as client:
        all_products = await client.check_product_list()
        print(f"\n📦 Total products in catalog: {all_products['total_products']}")
        
        departments = ["tools", "seeds", "decor", "irrigation"]
        for dept in departments:
            products = await client.check_product_list(department=dept)
            print(f"   - {dept.title()}: {len(products['products'])} products")


async def example_2_get_recommendations():
    print("\n" + "="*80)
    print("EXAMPLE 2: Get Personalized Recommendations")
    print("="*80)
    
    async with CustomerServicesMCPClient(mcp) as client:
        plant_types = ["Tomatoes", "Petunias", "Sunflowers"]
        
        for plant in plant_types:
            recs = await client.get_product_recommendations(
                plant_type=plant,
                customer_id="CUST-12345"
            )
            print(f"\n🌱 Recommendations for {plant}:")
            for rec in recs['recommendations'][:2]:
                print(f"   - {rec['name']}: £{rec['price']}")


async def example_3_check_availability():
    print("\n" + "="*80)
    print("EXAMPLE 3: Check Product Availability")
    print("="*80)
    
    async with CustomerServicesMCPClient(mcp) as client:
        products_to_check = [
            ("tool-001", "Hand Trowel"),
            ("seed-101", "Tomato Seeds"),
            ("decor-202", "Solar Garden Lantern")
        ]
        
        for product_id, name in products_to_check:
            availability = await client.check_product_availability(
                product_id=product_id,
                store_id="STORE-001"
            )
            
            status = "✅ Available" if availability['available'] else "❌ Out of Stock"
            qty = availability.get('quantity', 0)
            print(f"\n{status}: {name} (ID: {product_id})")
            if availability['available']:
                print(f"   Quantity: {qty} units")


async def example_4_shopping_workflow():
    print("\n" + "="*80)
    print("EXAMPLE 4: Complete Shopping Workflow")
    print("="*80)
    
    customer_id = "CUST-WORKFLOW-001"
    
    async with CustomerServicesMCPClient(mcp) as client:
        print("\n📋 Step 1: View current cart")
        cart = await client.access_cart_information(customer_id=customer_id)
        print(f"   Current cart total: £{cart['total']} ({cart['item_count']} items)")
        
        print("\n💡 Step 2: Get recommendations for tomatoes")
        recs = await client.get_product_recommendations(
            plant_type="Tomatoes",
            customer_id=customer_id
        )
        print(f"   Found {recs['total_recommendations']} recommendations")
        
        recommended_product = recs['recommendations'][0]
        print(f"\n📦 Step 3: Check availability of {recommended_product['name']}")
        availability = await client.check_product_availability(
            product_id=recommended_product['product_id'],
            store_id="STORE-001"
        )
        print(f"   Available: {availability['available']}")
        
        if availability['available']:
            print(f"\n➕ Step 4: Adding {recommended_product['name']} to cart")
            updated_cart = await client.modify_cart(
                customer_id=customer_id,
                items_to_add=[{
                    "product_id": recommended_product['product_id'],
                    "quantity": 2
                }]
            )
            cart_summary = updated_cart['cart_summary']
            print(f"   New cart total: £{cart_summary['total']} ({cart_summary['item_count']} items)")
        
        print("\n🛒 Step 5: View final cart")
        final_cart = await client.access_cart_information(customer_id=customer_id)
        print(f"   Items in cart: {final_cart['item_count']}")
        print(f"   Subtotal: £{final_cart['subtotal']}")
        print(f"   Tax: £{final_cart['tax']}")
        print(f"   Total: £{final_cart['total']}")


async def example_5_bulk_operations():
    print("\n" + "="*80)
    print("EXAMPLE 5: Bulk Operations")
    print("="*80)
    
    customer_id = "CUST-BULK-001"
    
    async with CustomerServicesMCPClient(mcp) as client:
        print("\n➕ Adding multiple items to cart")
        items_to_add = [
            {"product_id": "tool-001", "quantity": 2},
            {"product_id": "seed-101", "quantity": 5},
            {"product_id": "decor-201", "quantity": 1},
        ]
        
        cart = await client.modify_cart(
            customer_id=customer_id,
            items_to_add=items_to_add
        )
        
        print(f"   Added {len(items_to_add)} different products")
        print(f"   Cart total: £{cart['cart_summary']['total']}")
        
        print("\n➖ Removing items from cart")
        items_to_remove = [
            {"product_id": "tool-001", "quantity": 1},
        ]
        
        cart = await client.modify_cart(
            customer_id=customer_id,
            items_to_remove=items_to_remove
        )
        
        print(f"   Updated cart total: £{cart['cart_summary']['total']}")


async def example_6_error_handling():
    print("\n" + "="*80)
    print("EXAMPLE 6: Error Handling")
    print("="*80)
    
    async with CustomerServicesMCPClient(mcp) as client:
        print("\n❌ Attempting to access invalid department")
        result = await client.check_product_list(department="invalid_dept")
        if 'error' in result:
            print(f"   Error caught: {result['error']}")
            print(f"   Available departments: {', '.join(result['available_departments'])}")
        
        print("\n❌ Attempting to check non-existent product")
        result = await client.check_product_availability(
            product_id="invalid-999",
            store_id="STORE-001"
        )
        if 'error' in result:
            print(f"   Error caught: {result['error']}")


async def main():
    print("\n" + "🌟 "*30)
    print("MCP CLIENT - USAGE EXAMPLES")
    print("🌟 "*30)
    
    await example_1_browse_products()
    await example_2_get_recommendations()
    await example_3_check_availability()
    await example_4_shopping_workflow()
    await example_5_bulk_operations()
    await example_6_error_handling()
    
    print("\n" + "✅ "*30)
    print("ALL EXAMPLES COMPLETED")
    print("✅ "*30 + "\n")


if __name__ == "__main__":
    asyncio.run(main())