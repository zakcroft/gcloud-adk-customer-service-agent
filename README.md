
# Customer Services Agent

A customer service AI agent for Cymbal Home & Garden, built with Google ADK.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT SYSTEM MAP                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐
│   root_agent    │ ← Main Agent (Gemini 2.5 Flash)
│  "Project Pro"  │
└─────────┬───────┘
          │
          ├── GLOBAL_INSTRUCTION (Customer Profile: Alex Johnson)
          ├── INSTRUCTION (Core capabilities & constraints)
          │
          └── TOOLS ──┬── check_product_list
                      ├── get_product_recommendations  
                      ├── check_product_availability
                      ├── access_cart_information
                      └── modify_cart

┌─────────────────────────────────────────────────────────────┐
│                      TOOL DETAILS                           │
└─────────────────────────────────────────────────────────────┘

📦 check_product_list
   └── Returns products by department: tools, seeds, decor, irrigation

🎯 get_product_recommendations  
   └── Input: plant_type, customer_id
   └── Returns: tailored product suggestions

📊 check_product_availability
   └── Input: product_id, store_id
   └── Returns: stock status & quantity

🛒 access_cart_information
   └── Input: customer_id
   └── Returns: current cart contents & subtotal

✏️ modify_cart
   └── Input: customer_id, items_to_add, items_to_remove
   └── Returns: success status

┌─────────────────────────────────────────────────────────────┐
│                     CALLBACKS                               │
└─────────────────────────────────────────────────────────────┘

before_agent ──── Sets customer profile in session state
before_tool ───── Validates customer_id & applies business rules
after_tool ────── Post-processing (e.g., discount application)
rate_limit ────── Query rate limiting (10 RPM)

┌─────────────────────────────────────────────────────────────┐
│                   DATA ENTITIES                             │
└─────────────────────────────────────────────────────────────┘

Customer ──┬── Personal Info (Alex Johnson, #428765091)
           ├── Address (123 Main St, Anytown, CA)
           ├── Purchase History (3 past orders)
           ├── Garden Profile (backyard, medium, full sun)
           └── Loyalty Points (133)
```

## Flow

1. **Agent** receives user input
2. **before_agent** callback loads customer profile
3. **Agent** processes request using tools
4. **before_tool** validates customer access
5. **Tools** execute business logic
6. **after_tool** handles post-processing
7. **Agent** responds to user

## Setup

1. Copy `.env` file and configure:
   - `GOOGLE_GENAI_USE_VERTEXAI=1`
   - `GOOGLE_CLOUD_PROJECT=your-project`
   - `GOOGLE_CLOUD_LOCATION=us-central1`

2. Install dependencies:
   ```bash
   uv sync
   ```

## Key Files

- `agent/agent.py` - Main agent configuration
- `agent/prompts.py` - Agent instructions and personality
- `agent/tools/tools.py` - Business logic tools
- `agent/entities/customer.py` - Customer data models
- `agent/shared_libraries/callbacks.py` - Lifecycle callbacks