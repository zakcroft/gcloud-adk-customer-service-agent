import os
import sys


def serve():
    """Start the FastAPI server for local development."""
    # Add the project root to Python path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Import and run the FastAPI app
    from deploy.fast_api import app
    import uvicorn

    print("🚀 Starting Customer Services Agent API Server...")
    print("📖 API Documentation: http://localhost:8080/docs")
    print("🔍 Health Check: http://localhost:8080/health")
    print("\nPress CTRL+C to stop the server\n")

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")


def main():
    """Main entry point for CLI."""
    print("Starting customer services agent...")
    print("💡 To start the API server, run: uv run serve")


if __name__ == "__main__":
    main()
