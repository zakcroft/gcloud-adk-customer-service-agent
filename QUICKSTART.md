# Customer Services Agent - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### 1. Install Dependencies
```bash
uv sync
```

### 2. Configure Environment
Create a `.env` file with:
```bash
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

### 3. Start the Server
```bash
./serve.sh
```

That's it! Your API is now running at http://localhost:8080

---

## 📖 API Endpoints

### Health Check
```bash
curl http://localhost:8080/health
```

Response:
```json
{
  "status": "healthy",
  "service": "customer-services-agent",
  "version": "0.1.0"
}
```

### List Available Agents
```bash
curl http://localhost:8080/list-apps
```

### Interactive API Documentation
Open in your browser:
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

### Run a Query (Streaming)
```bash
curl -X POST http://localhost:8080/run_sse \
  -H "Content-Type: application/json" \
  -d '{
    "appName": "root_agent",
    "userMessage": "Do you sell seeds?",
    "userId": "test-user-123"
  }'
```

---

## 🛠️ Development Commands

### Start Server (2 Options)

**Option 1: Shell Script (Recommended)**
```bash
./serve.sh
```

**Option 2: Manual**
```bash
source .venv/bin/activate
PYTHONPATH=. python deploy/fast-api.py
```

> **Note**: `PYTHONPATH=.` is required so Python can find the `agent` module from the project root.

### Run Tests
```bash
source .venv/bin/activate
pytest
```

### Deploy to Cloud
```bash
./deploy.sh --deploy
```

---

## 🏗️ Project Structure

```
customer-services/
├── agents/                     # Agents directory (ADK standard)
│   └── root_agent/            # Root agent implementation
│       ├── __init__.py        # Agent module init
│       ├── agent.py           # Main agent definition (root_agent)
│       ├── prompts.py         # Instructions & personality
│       ├── config.py          # Configuration
│       ├── tools/             # Business logic tools
│       ├── entities/          # Data models
│       └── shared_libraries/  # Callbacks & utilities
├── deploy/                     # Deployment scripts
│   ├── fast-api.py            # FastAPI server
│   └── deploy.py              # Cloud deployment
├── serve.sh                    # Local server startup
├── deploy.sh                   # Cloud deployment wrapper
└── pyproject.toml             # Dependencies
```

**Note**: The `agents/` directory can contain multiple agents. Each agent lives in its own subdirectory with an `agent.py` file that defines `root_agent`.

---

## 🧪 Testing the Agent

### Example Conversation Flow

1. **Ask about products**
   ```bash
   curl -X POST http://localhost:8080/run_sse \
     -H "Content-Type: application/json" \
     -d '{"appName": "root_agent", "userMessage": "Do you sell seeds?", "userId": "u123"}'
   ```

2. **Get recommendations**
   ```bash
   curl -X POST http://localhost:8080/run_sse \
     -H "Content-Type: application/json" \
     -d '{"appName": "root_agent", "userMessage": "What vegetable seeds do you have?", "userId": "u123"}'
   ```

3. **Add to cart**
   ```bash
   curl -X POST http://localhost:8080/run_sse \
     -H "Content-Type: application/json" \
     -d '{"appName": "root_agent", "userMessage": "Add 2 packets of tomato seeds to my cart", "userId": "u123"}'
   ```

4. **Check cart**
   ```bash
   curl -X POST http://localhost:8080/run_sse \
     -H "Content-Type: application/json" \
     -d '{"appName": "root_agent", "userMessage": "What is in my cart?", "userId": "u123"}'
   ```

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if dependencies are installed
uv sync

# Check if port 8080 is already in use
lsof -i :8080

# Kill existing process on port 8080
kill -9 $(lsof -t -i:8080)
```

### Module not found errors
```bash
# Make sure PYTHONPATH is set
PYTHONPATH=. python deploy/fast-api.py

# Or use the serve.sh script which handles this automatically
./serve.sh
```

### Authentication errors
```bash
# Make sure you're authenticated with Google Cloud
gcloud auth application-default login

# Verify your project
gcloud config get-value project
```

---

## 📚 Next Steps

1. **Explore the API**: Open http://localhost:8080/docs
2. **Read the Architecture**: See `README.md` for system design
3. **Add Custom Tools**: Edit `agents/root_agent/tools/tools.py`
4. **Modify Instructions**: Edit `agents/root_agent/prompts.py`
5. **Deploy to Cloud**: Run `./deploy.sh --deploy`

---

## 🔗 Useful Links

- **ADK Documentation**: https://cloud.google.com/vertex-ai/docs/adk
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Vertex AI**: https://cloud.google.com/vertex-ai

