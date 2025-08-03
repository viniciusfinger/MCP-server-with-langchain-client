from service.customer_service import CustomerService
from service.order_service import OrderService
from server import mcp
import json
import logging

logger = logging.getLogger(__name__)

@mcp.tool()
def list_recent_customers_by_country(country: str, limit: int = 10) -> str:
    """
    List the top N (limit) most recent customers from a specific country

    Args:
        country (str): The country to list customers from (case sensitive, first char of country is uppercase)
        limit (int): The maximum number of customers to return (default: 10)

    Returns:
        Return a list of customers with id, name, joinedAt and totalSpend in a JSON format
    """
    logger.info(f"Listing recent customers by country: {country} with limit: {limit}")

    if not country:
        return json.dumps({"status": "invalid_arguments"})

    order_service = OrderService()
    customer_service = CustomerService()

    recent_customers = customer_service.list_recent_customers_by_country(country, limit)
    logger.info(f"Found {len(recent_customers)} customers")

    customer_ids = [customer.id for customer in recent_customers]
    totals = order_service.calculate_aggregate_spending_for_customers(customer_ids)
    
    customers = [
        {
            "id": customer.id,
            "name": customer.name,
            "joinedAt": customer.joined_at.isoformat(),
            "totalSpend": totals[customer.id] if customer.id in totals else 0
        }
        for customer in recent_customers
    ]

    return json.dumps({"customers": customers})


@mcp.tool()
def get_customer_total_spend(customer_ids: list[int]) -> str:
    """
    Get the total spend for a list of customers

    Args:
        customer_ids (list[int]): The list of customer IDs to get the total spend for

    Returns:
        The total spend for the list of customers in a JSON format, with customerId and spend
    """
    logger.info(f"Getting total spend for customer IDs: {customer_ids}")
    
    if not customer_ids:
        logger.warning("No customer IDs provided")
        return json.dumps({"status": "invalid_arguments"})
    
    for customer_id in customer_ids:
        if not isinstance(customer_id, int):
            logger.warning(f"Invalid customer ID type: {type(customer_id)} for ID: {customer_id}")
            return json.dumps({"status": "invalid_arguments"})

    order_service = OrderService()
    totals = order_service.calculate_aggregate_spending_for_customers(customer_ids)
    
    logger.info(f"Calculated totals: {totals}")
    return json.dumps({"totals": totals})


@mcp.tool()
def get_customer_id_by_name(customer_name: str) -> str:
    """
    Get a customer ID by their name (case sensitive, first char of name and surname is uppercase)

    Args:
        customer_name (str): The name of the customer (case sensitive, first char of name and surname is uppercase)

    Returns:
        The customer ID in a JSON format
    """
    logger.info(f"Getting customer ID by name: {customer_name}")

    customer_service = CustomerService()
    customer_id = customer_service.get_customer_id_by_name(customer_name)

    if customer_id is None:
        return json.dumps({"status": "customer_not_found"})

    return json.dumps({"customerId": customer_id})