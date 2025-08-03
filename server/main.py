from server import mcp
from config.logging_config import setup_logging

import tools.customer_tools
import tools.order_tools

if __name__ == "__main__":
    setup_logging()
    mcp.run(transport="streamable-http")
