import logging
from typing import Optional

logger = logging.getLogger(__name__)


def check_product_list(department: Optional[str] = None) -> dict:
    """Get a list of products by department or all products.

    Args:
        department: Optional department filter (tools, seeds, decor, irrigation)

    Returns:
        Dictionary with products list and metadata
    """
    products = [
        # Tools Department
        {
            "product_id": "tool-001",
            "name": "Hand Trowel",
            "description": "Durable steel trowel for planting and transplanting.",
            "department": "tools",
            "price": 12.99,
            "in_stock": True,
            "stock_quantity": 45,
        },
        {
            "product_id": "tool-002",
            "name": "Pruning Shears",
            "description": "Sharp bypass pruners for trimming stems and branches.",
            "department": "tools",
            "price": 24.99,
            "in_stock": True,
            "stock_quantity": 23,
        },
        {
            "product_id": "tool-003",
            "name": "Garden Spade",
            "description": "Heavy-duty spade for digging and soil preparation.",
            "department": "tools",
            "price": 34.99,
            "in_stock": True,
            "stock_quantity": 12,
        },

        # Seeds Department
        {
            "product_id": "seed-101",
            "name": "Tomato Seeds - Cherry",
            "description": "Heirloom cherry tomato seeds for sweet, juicy fruits.",
            "department": "seeds",
            "price": 3.99,
            "in_stock": True,
            "stock_quantity": 156,
        },
        {
            "product_id": "seed-102",
            "name": "Sunflower Seeds - Giant",
            "description": "Tall, vibrant yellow sunflowers that attract pollinators.",
            "department": "seeds",
            "price": 4.99,
            "in_stock": True,
            "stock_quantity": 89,
        },
        {
            "product_id": "seed-103",
            "name": "Petunia Seeds - Mixed Colors",
            "description": "Colorful annual flowers perfect for containers and borders.",
            "department": "seeds",
            "price": 5.99,
            "in_stock": True,
            "stock_quantity": 67,
        },

        # Decor Department
        {
            "product_id": "decor-201",
            "name": "Terracotta Planter - Large",
            "description": "Classic clay pot ideal for indoor and outdoor plants.",
            "department": "decor",
            "price": 18.99,
            "in_stock": True,
            "stock_quantity": 34,
        },
        {
            "product_id": "decor-202",
            "name": "Solar Garden Lantern",
            "description": "Solar-powered lantern to add charm to your garden.",
            "department": "decor",
            "price": 29.99,
            "in_stock": False,
            "stock_quantity": 0,
        },
        {
            "product_id": "decor-203",
            "name": "Garden Stepping Stones",
            "description": "Natural stone path markers for garden walkways.",
            "department": "decor",
            "price": 39.99,
            "in_stock": True,
            "stock_quantity": 18,
        },

        # Irrigation Department
        {
            "product_id": "irrig-301",
            "name": "Soaker Hose - 25ft",
            "description": "Efficient watering system for garden beds.",
            "department": "irrigation",
            "price": 19.99,
            "in_stock": True,
            "stock_quantity": 28,
        },
        {
            "product_id": "irrig-302",
            "name": "Copper Watering Can",
            "description": "Metal watering can with a long spout for gentle watering.",
            "department": "irrigation",
            "price": 42.99,
            "in_stock": True,
            "stock_quantity": 15,
        },
    ]

    if department is not None:
        department = department.lower()
        filtered = [p for p in products if p["department"] == department]
        if not filtered:
            return {
                "error": f"No products found for department '{department}'",
                "available_departments": ["tools", "seeds", "decor", "irrigation"],
                "products": []
            }
        return {
            "department": department,
            "total_products": len(filtered),
            "products": filtered
        }

    return {
        "department": "all",
        "total_products": len(products),
        "products": products
    }


def get_product_recommendations(plant_type: str, customer_id: str) -> dict:
    """Provides product recommendations based on the type of plant and customer profile.

    Args:
        plant_type: The type of plant (e.g., 'Petunias', 'Sun-loving annuals', 'Tomatoes').
        customer_id: Customer ID for personalized recommendations.

    Returns:
        A dictionary of recommended products with pricing and availability.
    """
    logger.info(
        "Getting product recommendations for plant type: %s and customer %s",
        plant_type,
        customer_id,
    )

    # Enhanced recommendation engine with more plant types and realistic products
    plant_type_lower = plant_type.lower()

    # Define comprehensive product database for recommendations
    recommendation_db = {
        "petunias": {
            "recommendations": [
                {
                    "product_id": "soil-456",
                    "name": "Bloom Booster Potting Mix",
                    "description": "Premium potting mix with extra nutrients that Petunias love for continuous blooming.",
                    "price": 14.99,
                    "in_stock": True,
                    "stock_quantity": 42,
                    "category": "soil"
                },
                {
                    "product_id": "fert-789",
                    "name": "Flower Power Fertilizer",
                    "description": "Specifically formulated for flowering annuals with balanced NPK ratio.",
                    "price": 9.99,
                    "in_stock": True,
                    "stock_quantity": 67,
                    "category": "fertilizer"
                },
                {
                    "product_id": "tool-004",
                    "name": "Deadheading Snips",
                    "description": "Precision snips perfect for deadheading petunias to encourage more blooms.",
                    "price": 16.99,
                    "in_stock": True,
                    "stock_quantity": 23,
                    "category": "tools"
                }
            ]
        },
        "tomatoes": {
            "recommendations": [
                {
                    "product_id": "soil-789",
                    "name": "Vegetable Garden Soil",
                    "description": "Rich, organic soil blend perfect for tomatoes and other vegetables.",
                    "price": 12.99,
                    "in_stock": True,
                    "stock_quantity": 38,
                    "category": "soil"
                },
                {
                    "product_id": "fert-456",
                    "name": "Tomato & Vegetable Fertilizer",
                    "description": "Specially formulated for tomatoes with calcium to prevent blossom end rot.",
                    "price": 11.99,
                    "in_stock": True,
                    "stock_quantity": 45,
                    "category": "fertilizer"
                },
                {
                    "product_id": "supp-101",
                    "name": "Tomato Cages - Set of 3",
                    "description": "Sturdy wire cages to support growing tomato plants.",
                    "price": 24.99,
                    "in_stock": True,
                    "stock_quantity": 19,
                    "category": "support"
                }
            ]
        },
        "sunflowers": {
            "recommendations": [
                {
                    "product_id": "soil-123",
                    "name": "All-Purpose Garden Soil",
                    "description": "Well-draining soil perfect for sunflowers and other tall plants.",
                    "price": 10.99,
                    "in_stock": True,
                    "stock_quantity": 56,
                    "category": "soil"
                },
                {
                    "product_id": "fert-321",
                    "name": "High Nitrogen Fertilizer",
                    "description": "Promotes strong stem growth for tall plants like sunflowers.",
                    "price": 13.99,
                    "in_stock": True,
                    "stock_quantity": 31,
                    "category": "fertilizer"
                }
            ]
        }
    }

    # Check for specific plant type matches
    for plant_key in recommendation_db.keys():
        if plant_key in plant_type_lower:
            result = recommendation_db[plant_key].copy()
            result["plant_type"] = plant_type
            result["customer_id"] = customer_id
            result["total_recommendations"] = len(result["recommendations"])
            return result

    # Handle general categories
    if any(term in plant_type_lower for term in ["annual", "flower", "bloom"]):
        result = recommendation_db["petunias"].copy()
        result["plant_type"] = plant_type
        result["customer_id"] = customer_id
        result["total_recommendations"] = len(result["recommendations"])
        result["note"] = "General flowering plant recommendations"
        return result

    if any(term in plant_type_lower for term in ["vegetable", "veggie", "edible"]):
        result = recommendation_db["tomatoes"].copy()
        result["plant_type"] = plant_type
        result["customer_id"] = customer_id
        result["total_recommendations"] = len(result["recommendations"])
        result["note"] = "General vegetable gardening recommendations"
        return result

    # Default general recommendations
    general_recommendations = {
        "plant_type": plant_type,
        "customer_id": customer_id,
        "recommendations": [
            {
                "product_id": "soil-123",
                "name": "All-Purpose Garden Soil",
                "description": "Versatile potting soil suitable for most plants.",
                "price": 10.99,
                "in_stock": True,
                "stock_quantity": 56,
                "category": "soil"
            },
            {
                "product_id": "fert-general",
                "name": "General Purpose Plant Food",
                "description": "Balanced fertilizer suitable for a wide variety of plants.",
                "price": 8.99,
                "in_stock": True,
                "stock_quantity": 73,
                "category": "fertilizer"
            }
        ],
        "total_recommendations": 2,
        "note": "General gardening recommendations - consider providing more specific plant information for better suggestions"
    }

    return general_recommendations


def check_product_availability(product_id: str, store_id: str) -> dict:
    """Checks the availability of a product at a specified store or for pickup.

    Args:
        product_id: The ID of the product to check.
        store_id: The ID of the store or 'pickup' for pickup availability.

    Returns:
        A dictionary indicating availability with detailed stock information.
    """
    logger.info(
        "Checking availability of product ID: %s at store: %s",
        product_id,
        store_id,
    )

    # Realistic inventory database
    inventory = {
        # From product list
        "tool-001": {"quantity": 45, "reserved": 3, "available": 42},
        "tool-002": {"quantity": 23, "reserved": 1, "available": 22},
        "tool-003": {"quantity": 12, "reserved": 0, "available": 12},
        "seed-101": {"quantity": 156, "reserved": 8, "available": 148},
        "seed-102": {"quantity": 89, "reserved": 4, "available": 85},
        "seed-103": {"quantity": 67, "reserved": 2, "available": 65},
        "decor-201": {"quantity": 34, "reserved": 1, "available": 33},
        "decor-202": {"quantity": 0, "reserved": 0, "available": 0},  # Out of stock
        "decor-203": {"quantity": 18, "reserved": 2, "available": 16},
        "irrig-301": {"quantity": 28, "reserved": 3, "available": 25},
        "irrig-302": {"quantity": 15, "reserved": 1, "available": 14},

        # From recommendations
        "soil-456": {"quantity": 42, "reserved": 2, "available": 40},
        "fert-789": {"quantity": 67, "reserved": 5, "available": 62},
        "tool-004": {"quantity": 23, "reserved": 1, "available": 22},
        "soil-789": {"quantity": 38, "reserved": 3, "available": 35},
        "fert-456": {"quantity": 45, "reserved": 2, "available": 43},
        "supp-101": {"quantity": 19, "reserved": 1, "available": 18},
        "soil-123": {"quantity": 56, "reserved": 4, "available": 52},
        "fert-321": {"quantity": 31, "reserved": 2, "available": 29},
        "fert-general": {"quantity": 73, "reserved": 3, "available": 70},
    }

    if product_id not in inventory:
        return {
            "available": False,
            "error": f"Product ID '{product_id}' not found in inventory",
            "product_id": product_id,
            "store": store_id
        }

    stock_info = inventory[product_id]
    available_qty = stock_info["available"]

    # Determine availability status
    if available_qty == 0:
        status = "out_of_stock"
        available = False
    elif available_qty <= 5:
        status = "low_stock"
        available = True
    else:
        status = "in_stock"
        available = True

    return {
        "available": available,
        "quantity": available_qty,
        "total_quantity": stock_info["quantity"],
        "reserved": stock_info["reserved"],
        "status": status,
        "store": store_id,
        "product_id": product_id,
        "message": f"{'Available' if available else 'Out of stock'} at {store_id}"
    }


# Global cart state for simulation (in production, this would be in a database)
_CART_STATE = {}

def access_cart_information(customer_id: str) -> dict:
    """Retrieves the current cart contents for a customer.

    Args:
        customer_id (str): The ID of the customer.

    Returns:
        dict: A dictionary representing the cart contents with detailed pricing.
    """
    logger.info("Accessing cart information for customer ID: %s", customer_id)

    # Initialize cart if it doesn't exist
    if customer_id not in _CART_STATE:
        _CART_STATE[customer_id] = [
            {
                "product_id": "soil-123",
                "name": "All-Purpose Garden Soil",
                "description": "Versatile potting soil suitable for most plants.",
                "quantity": 2,
                "unit_price": 10.99,
                "department": "soil"
            },
            {
                "product_id": "seed-101",
                "name": "Tomato Seeds - Cherry",
                "description": "Heirloom cherry tomato seeds for sweet, juicy fruits.",
                "quantity": 1,
                "unit_price": 3.99,
                "department": "seeds"
            }
        ]

    # Get current cart items
    cart_items = _CART_STATE[customer_id]

    # Calculate totals
    subtotal = sum(item["quantity"] * item["unit_price"] for item in cart_items)
    tax = round(subtotal * 0.08, 2)  # 8% tax
    total = round(subtotal + tax, 2)
    item_count = sum(item["quantity"] for item in cart_items)

    # Add total_price to each item
    for item in cart_items:
        item["total_price"] = round(item["quantity"] * item["unit_price"], 2)

    cart_response = {
        "customer_id": customer_id,
        "items": cart_items,
        "item_count": item_count,
        "unique_items": len(cart_items),
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "currency": "GBP",
        "last_updated": "2024-01-15T10:30:00Z"
    }

    return cart_response


def modify_cart(
    customer_id: str, items_to_add: list[dict], items_to_remove: list[dict]
) -> dict:
    """Modifies the user's shopping cart by adding and/or removing items.

    Args:
        customer_id (str): The ID of the customer.
        items_to_add (list): List of dicts with 'product_id' and 'quantity' keys.
        items_to_remove (list): List of dicts with 'product_id' and 'quantity' keys.

    Returns:
        dict: Detailed status of the cart modification with updated totals.
    """
    logger.info("Modifying cart for customer ID: %s", customer_id)
    logger.info("Adding items: %s", items_to_add)
    logger.info("Removing items: %s", items_to_remove)

    # Product database for lookups
    product_database = {
        "tool-001": {"name": "Hand Trowel", "price": 12.99, "department": "tools"},
        "tool-002": {"name": "Pruning Shears", "price": 24.99, "department": "tools"},
        "tool-003": {"name": "Garden Spade", "price": 34.99, "department": "tools"},
        "seed-101": {"name": "Tomato Seeds - Cherry", "price": 3.99, "department": "seeds"},
        "seed-102": {"name": "Sunflower Seeds - Giant", "price": 4.99, "department": "seeds"},
        "seed-103": {"name": "Petunia Seeds - Mixed Colors", "price": 5.99, "department": "seeds"},
        "decor-201": {"name": "Terracotta Planter - Large", "price": 18.99, "department": "decor"},
        "decor-202": {"name": "Solar Garden Lantern", "price": 29.99, "department": "decor"},
        "decor-203": {"name": "Garden Stepping Stones", "price": 39.99, "department": "decor"},
        "irrig-301": {"name": "Soaker Hose - 25ft", "price": 19.99, "department": "irrigation"},
        "irrig-302": {"name": "Copper Watering Can", "price": 42.99, "department": "irrigation"},
        "soil-456": {"name": "Bloom Booster Potting Mix", "price": 14.99, "department": "soil"},
        "fert-789": {"name": "Flower Power Fertilizer", "price": 9.99, "department": "fertilizer"},
        "tool-004": {"name": "Deadheading Snips", "price": 16.99, "department": "tools"},
        "soil-789": {"name": "Vegetable Garden Soil", "price": 12.99, "department": "soil"},
        "fert-456": {"name": "Tomato & Vegetable Fertilizer", "price": 11.99, "department": "fertilizer"},
        "supp-101": {"name": "Tomato Cages - Set of 3", "price": 24.99, "department": "support"},
        "soil-123": {"name": "All-Purpose Garden Soil", "price": 10.99, "department": "soil"},
        "fert-321": {"name": "High Nitrogen Fertilizer", "price": 13.99, "department": "fertilizer"},
        "fert-general": {"name": "General Purpose Plant Food", "price": 8.99, "department": "fertilizer"}
    }

    # Initialize cart if it doesn't exist
    if customer_id not in _CART_STATE:
        _CART_STATE[customer_id] = []

    # Get current cart
    current_cart = _CART_STATE[customer_id]

    # Track modifications
    added_items = []
    removed_items = []
    errors = []

    # Process removals first
    for item in items_to_remove:
        product_id = item.get("product_id")
        quantity_to_remove = item.get("quantity", 1)

        if not product_id:
            errors.append("Missing product_id in items_to_remove")
            continue

        # Find item in cart
        cart_item = None
        for cart_item_ref in current_cart:
            if cart_item_ref["product_id"] == product_id:
                cart_item = cart_item_ref
                break

        if not cart_item:
            errors.append(f"Product {product_id} not found in cart")
            continue

        # Remove quantity
        if cart_item["quantity"] <= quantity_to_remove:
            # Remove entire item
            current_cart.remove(cart_item)
            removed_items.append({
                "product_id": product_id,
                "quantity": cart_item["quantity"],
                "name": cart_item["name"]
            })
        else:
            # Reduce quantity
            cart_item["quantity"] -= quantity_to_remove
            removed_items.append({
                "product_id": product_id,
                "quantity": quantity_to_remove,
                "name": cart_item["name"]
            })

    # Process additions
    for item in items_to_add:
        product_id = item.get("product_id")
        quantity = item.get("quantity", 1)

        if not product_id:
            errors.append("Missing product_id in items_to_add")
            continue

        if product_id not in product_database:
            errors.append(f"Product {product_id} not found")
            continue

        # Check availability (simplified - in production would call inventory service)
        if product_id == "decor-202":  # Out of stock item
            errors.append(f"Product {product_id} is out of stock")
            continue

        product_info = product_database[product_id]

        # Check if item already exists in cart
        existing_item = None
        for cart_item in current_cart:
            if cart_item["product_id"] == product_id:
                existing_item = cart_item
                break

        if existing_item:
            # Update quantity
            existing_item["quantity"] += quantity
            added_items.append({
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": product_info["price"],
                "total_price": product_info["price"] * quantity,
                "name": product_info["name"]
            })
        else:
            # Add new item
            new_cart_item = {
                "product_id": product_id,
                "name": product_info["name"],
                "description": f"{product_info['name']} from {product_info['department']} department",
                "quantity": quantity,
                "unit_price": product_info["price"],
                "department": product_info["department"]
            }
            current_cart.append(new_cart_item)
            added_items.append({
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": product_info["price"],
                "total_price": product_info["price"] * quantity,
                "name": product_info["name"]
            })

    # Calculate new totals
    subtotal = sum(item["quantity"] * item["unit_price"] for item in current_cart)
    tax = round(subtotal * 0.08, 2)  # 8% tax
    total = round(subtotal + tax, 2)

    result = {
        "status": "success" if not errors else "partial_success",
        "customer_id": customer_id,
        "modifications": {
            "items_added": added_items,
            "items_removed": removed_items,
            "total_added": len(added_items),
            "total_removed": len(removed_items)
        },
        "cart_summary": {
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
            "currency": "GBP",
            "item_count": sum(item["quantity"] for item in current_cart),
            "unique_items": len(current_cart)
        },
        "message": f"Cart updated: {len(added_items)} items added, {len(removed_items)} items removed",
        "errors": errors if errors else None
    }

    if errors:
        result["message"] += f" with {len(errors)} errors"

    return result
