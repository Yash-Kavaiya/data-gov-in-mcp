"""
data.gov.in MCP Server - Entry Point

A production-ready Model Context Protocol server for accessing
Indian government open data from data.gov.in.

Features:
- Dataset retrieval with pagination
- Field schema inspection
- Filtering and searching
- Response caching
- Rate limiting
- Error handling and retries
- Comprehensive logging

Usage:
    python main.py

Environment Variables:
    DATA_GOV_IN_API_KEY - Your data.gov.in API key (required)
    DATA_GOV_IN_BASE_URL - API base URL (default: https://api.data.gov.in)
    DATA_GOV_IN_CACHE_ENABLED - Enable caching (default: true)
    DATA_GOV_IN_LOG_LEVEL - Logging level (default: INFO)

Author: Data.gov.in MCP Team
Version: 1.0.0
License: MIT
"""

from src.data_gov_in.server import run_server

if __name__ == "__main__":
    run_server()
