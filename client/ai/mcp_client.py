from langchain_mcp_adapters.client import MultiServerMCPClient
import os
from dotenv import load_dotenv
load_dotenv()


def get_mcp_client():
    return MultiServerMCPClient(
        {
            "simple_server": {
                "url": os.getenv("MCP_SERVER_URL"),
                "transport": "streamable_http"
            }
        }
    )