from model.customer import Customer
import json


class CustomerService:
    def __init__(self, file_path: str = "data/customers.json"):
        self.customers = self.load_customers(file_path)

    def load_customers(self, file_path: str) -> list[Customer]:
        with open(file_path, "r") as file:
            return [Customer(**customer) for customer in json.load(file)]
    
    def list_recent_customers_by_country(self, country: str, limit: int = 10) -> list[Customer]:
        customers_from_country = [
            customer for customer in self.customers 
            if customer.country == country
        ]
        
        sorted_customers = sorted(
            customers_from_country,
            key=lambda customer: customer.joined_at,
            reverse=True
        )
        
        return sorted_customers[:limit]
    
    def get_customer_id_by_name(self, customer_name: str) -> int:
        return next((customer.id for customer in self.customers if customer.name == customer_name), None)