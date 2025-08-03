from model.order import Order
import json
from typing import List, Dict


class OrderService:
    def __init__(self, file_path: str = "data/orders.json"):
        self.orders = self.load_orders(file_path)

    def load_orders(self, file_path: str) -> list[Order]:
        with open(file_path, "r") as file:
            return [Order(**order) for order in json.load(file)]

    def get_order_count_by_customer_and_month(self, customer_name: str, iso_month: str) -> int:
        return len(list(filter(lambda order: order.customer_name == customer_name and order.date.strftime("%Y-%m") == iso_month, self.orders)))

    def calculate_aggregate_spending_for_customers(self, customer_ids: List[int]) -> List[Dict[str, any]]:
        customer_ids_set = set(customer_ids)
        
        spending_by_customer = {}
        
        for order in self.orders:
            if order.customer_id in customer_ids_set:
                if order.customer_id not in spending_by_customer:
                    spending_by_customer[order.customer_id] = 0
                spending_by_customer[order.customer_id] += order.amount
        
        result = []
        for customer_id in customer_ids:
            result.append({
                "customerId": customer_id,
                "spend": float(spending_by_customer.get(customer_id, 0))
            })
        
        return result
