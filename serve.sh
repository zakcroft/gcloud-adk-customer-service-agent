#!/bin/bash

# Customer Service Agent API Server Startup Script
# This script starts the FastAPI server for local development

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Customer Services Agent - API Server${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}❌ Virtual environment not found.${NC}"
    echo -e "${YELLOW}💡 Please run 'uv sync' first to install dependencies.${NC}"
    exit 1
fi

# Check if dependencies are installed
if [ ! -f ".venv/bin/uvicorn" ]; then
    echo -e "${YELLOW}⚠️  Dependencies not fully installed.${NC}"
    echo -e "${YELLOW}💡 Running 'uv sync' to install dependencies...${NC}\n"
    uv sync
fi

echo -e "${GREEN}✓ Virtual environment found${NC}"
echo -e "${GREEN}✓ Starting FastAPI server...${NC}"
echo -e "${GREEN}📖 API Documentation: http://localhost:8080/docs${NC}"
echo -e "${GREEN}🔍 Health Check: http://localhost:8080/health${NC}\n"

# Activate virtual environment and start the server with PYTHONPATH set
source .venv/bin/activate
PYTHONPATH=. python deploy/fast-api.py

