
# Customer Services Agent

A customer service AI agent for Cymbal Home & Garden, built with Google ADK.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT SYSTEM MAP                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐
│   root_agent    │ ← Main Agent (Gemini 2.5 Flash)
│  "Project Pro"  │   Located in: agents/root_agent/
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

## Local Development

### Code Formatting

Format Python code with Ruff:

```bash
# Format all Python files
ruff format app/ eval/ deploy/

# Check and auto-fix linting issues
ruff check app/ eval/ deploy/ --fix
```

### Running the MCP Server

Start the FastMCP server to expose tools via the Model Context Protocol:

```bash
# Run the MCP server
uv run python -m mcp_server.fast_mcp_server

# Or activate the virtual environment first
source .venv/bin/activate
python -m mcp_server.fast_mcp_server
```

This exposes all customer service tools (check_product_list, get_product_recommendations, etc.) via MCP, making them available to any MCP-compatible client.

**Available Tools:**
- `check_product_list` - Get products by department
- `get_product_recommendations` - Get personalized product recommendations
- `check_product_availability` - Check stock availability
- `access_cart_information` - Retrieve customer cart
- `modify_cart` - Add/remove items from cart

**Query Available Tools:**
```bash
python query_mcp_tools.py
```

### Running the FastAPI Server

Start the local development server:

```bash
# Option 1: Using the convenience script (Recommended)
./serve.sh

# Option 2: Manual activation
source .venv/bin/activate
PYTHONPATH=. python deploy/fast-api.py
```

**Why `PYTHONPATH=.`?** This tells Python to look in the current directory for modules, allowing `deploy/fast-api.py` to import from the `agent/` directory.

The server will start on `http://localhost:8080`:
- 📖 **API Documentation**: http://localhost:8080/docs
- 🔍 **Health Check**: http://localhost:8080/health
- 🎯 **OpenAPI Spec**: http://localhost:8080/openapi.json

### Testing the API

```bash
# Health check
curl http://localhost:8080/health

# List available agents
curl http://localhost:8080/list-apps

# Run a query (streaming)
curl -X POST http://localhost:8080/run_sse \
  -H "Content-Type: application/json" \
  -d '{
    "appName": "root_agent",
    "userMessage": "Do you sell seeds?",
    "userId": "test-user-123"
  }'
```

## Cloud Deployment

Use the consolidated deployment script for all operations. You can use either the shell wrapper or call Python directly:

### Option 1: Shell Wrapper (Recommended)
```bash
# Deploy the agent
./deploy.sh --deploy

# List all deployed agents
./deploy.sh --list

# Test a deployed agent
./deploy.sh --test <resource_name>

# Delete a deployed agent
./deploy.sh --delete <resource_name>

# Enable verbose logging
./deploy.sh --deploy --verbose
```

### Option 2: Direct Python Call
```bash
# Activate environment and set Python path
source .venv/bin/activate
PYTHONPATH=. python deploy/deploy.py --deploy
```

### Available Commands
- `--deploy`: Deploy the customer service agent to Vertex AI Agent Engine
- `--list`: List all deployed agents in your project with details
- `--test <resource_name>`: Test a deployed agent with sample customer queries
- `--delete <resource_name>`: Delete a deployed agent
- `--verbose`: Enable detailed logging for troubleshooting

## Key Files

- `agents/root_agent/agent.py` - Main agent configuration
- `agents/root_agent/prompts.py` - Agent instructions and personality
- `agents/root_agent/tools/tools.py` - Business logic tools
- `agents/root_agent/entities/customer.py` - Customer data models
- `agents/root_agent/shared_libraries/callbacks.py` - Lifecycle callbacks