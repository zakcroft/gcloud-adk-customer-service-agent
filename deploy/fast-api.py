
import os
from google.adk.cli.fast_api import get_fast_api_app
from fastapi import FastAPI

DEPLOY_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.join(os.path.dirname(DEPLOY_DIR), "app")

print('AGENT_DIR===', AGENT_DIR)

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
    trace_to_cloud=True,
)

app.title = "customer-services-agent"
app.description = "API for interacting with the customer services Agent."


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "customer-services-agent",
        "version": "0.1.0"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)