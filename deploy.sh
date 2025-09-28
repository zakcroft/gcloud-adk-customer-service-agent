#!/bin/bash

# Customer Service Agent Deployment Script
# This script provides a convenient wrapper for the Python deployment tool

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run 'uv sync' first."
    exit 1
fi

# Activate virtual environment and run the deployment script with proper Python path
source .venv/bin/activate
PYTHONPATH=. python deploy/deploy.py "$@"
