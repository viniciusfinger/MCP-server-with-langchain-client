from server import mcp
from service.order_service import OrderService
import json
import logging

logger = logging.getLogger(__name__)

@mcp.tool()
def get_order_count_by_customer_and_month(customer_name: str, month: str) -> str:
    """
    Count orders for one customer in a specific calendar month

    Args:
        customer_name (str): The name of the customer (case sensitive, first char of name and surname is uppercase)
        month (str): ISO 8601 format (YYYY-MM)

    Returns:
        The number of orders for the customer in the specified month in a JSON format
    """
    logger.info(f"Getting order count for customer: {customer_name} in month: {month}")

    if not customer_name:
        return json.dumps({"status": "invalid_arguments"})
    
    if not month:
        return json.dumps({"status": "invalid_arguments"})

    order_service = OrderService()
    order_count = order_service.get_order_count_by_customer_and_month(customer_name, month)
    
    logger.info(f"Found {order_count} orders for customer {customer_name} in month {month}")
    return json.dumps({"count": order_count})