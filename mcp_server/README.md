# MCP Server & Client for Customer Services

This directory contains a complete Model Context Protocol (MCP) implementation for the Customer Services agent, including both server and client implementations.

## 📁 Files Overview

### Server Files
- **`server.py`** - Low-level MCP server using `mcp.server.lowlevel`
- **`fast_mcp_server.py`** - FastMCP server implementation (recommended)

### Client Files
- **`fast_mcp_client.py`** - Full-featured programmatic client with all tools
- **`interactive_client.py`** - Interactive command-line interface


## 🚀 Quick Start

### 1. Start the Server

```bash
# Using FastMCP (recommended)
python -m mcp_server.fast_mcp_server
  
```