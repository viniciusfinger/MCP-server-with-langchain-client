import pytest
import json
import tempfile
import os
from datetime import datetime
from unittest.mock import patch, mock_open
from service.customer_service import CustomerService
from model.customer import Customer


class TestCustomerService:

    @pytest.fixture
    def sample_customers_data(self):
        return [
            {
                "id": 1,
                "name": "John Doe",
                "country": "USA",
                "joinedAt": "2024-01-15T10:30:00Z"
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "country": "USA",
                "joinedAt": "2024-02-20T14:45:00Z"
            },
            {
                "id": 3,
                "name": "Carlos Rodriguez",
                "country": "Brazil",
                "joinedAt": "2024-03-05T09:15:00Z"
            },
            {
                "id": 4,
                "name": "Maria Silva",
                "country": "Brazil",
                "joinedAt": "2024-04-10T16:20:00Z"
            },
            {
                "id": 5,
                "name": "Ronaldinho Gaucho",
                "country": "Brazil",
                "joinedAt": "2024-05-11T16:20:00Z"
            },
            {
                "id": 6,
                "name": "Pierre Dupont",
                "country": "France",
                "joinedAt": "2024-05-12T11:00:00Z"
            },
            {
                "id": 7,
                "name": "Sophie Martin",
                "country": "France",
                "joinedAt": "2024-06-18T13:40:00Z"
            },
            {
                "id": 8,
                "name": "Hiroshi Tanaka",
                "country": "Japan",
                "joinedAt": "2024-07-22T08:50:00Z"
            }
        ]

    @pytest.fixture
    def temp_customers_file(self, sample_customers_data):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sample_customers_data, f)
            temp_file_path = f.name
        
        yield temp_file_path
        
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

    def test_init_with_default_file_path(self):
        with patch('builtins.open', mock_open(read_data='[]')):
            service = CustomerService()
            assert service.customers == []

    def test_init_with_custom_file_path(self):
        custom_path = "custom/path/customers.json"
        with patch('builtins.open', mock_open(read_data='[]')):
            service = CustomerService(custom_path)
            assert service.customers == []

    def test_load_customers_success(self, temp_customers_file):
        service = CustomerService(temp_customers_file)
        
        assert len(service.customers) == 8
        assert all(isinstance(customer, Customer) for customer in service.customers)
        
        first_customer = service.customers[0]
        assert first_customer.id == 1
        assert first_customer.name == "John Doe"
        assert first_customer.country == "USA"
        assert isinstance(first_customer.joined_at, datetime)

    def test_load_customers_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            CustomerService("arquivo_inexistente.json")

    def test_load_customers_invalid_json(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": json}')
            temp_file_path = f.name
        
        try:
            with pytest.raises(json.JSONDecodeError):
                CustomerService(temp_file_path)
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_list_recent_customers_by_country_exact_match(self, temp_customers_file):
        service = CustomerService(temp_customers_file)
        
        brazil_customers = service.list_recent_customers_by_country("Brazil")
        assert len(brazil_customers) == 3
        assert all(customer.country == "Brazil" for customer in brazil_customers)
        
        assert brazil_customers[0].name == "Ronaldinho Gaucho"
        assert brazil_customers[1].name == "Maria Silva"
        assert brazil_customers[2].name == "Carlos Rodriguez"

    def test_list_recent_customers_by_country_no_match(self, temp_customers_file):
        service = CustomerService(temp_customers_file)
        
        customers = service.list_recent_customers_by_country("Canada")
        assert len(customers) == 0

    def test_list_recent_customers_by_country_case_sensitive(self, temp_customers_file):
        service = CustomerService(temp_customers_file)
        
        customers = service.list_recent_customers_by_country("brazil")
        assert len(customers) == 0

    def test_list_recent_customers_by_country_with_limit(self, temp_customers_file):
        service = CustomerService(temp_customers_file)
        
        brazil_customers = service.list_recent_customers_by_country("Brazil", limit=2)
        assert len(brazil_customers) == 2
        assert brazil_customers[0].name == "Ronaldinho Gaucho"
        assert brazil_customers[1].name == "Maria Silva"
        
        usa_customers = service.list_recent_customers_by_country("USA", limit=10)
        assert len(usa_customers) == 2

    def test_list_recent_customers_by_country_default_limit(self, temp_customers_file):
        service = CustomerService(temp_customers_file)
        
        usa_customers = service.list_recent_customers_by_country("USA")
        assert len(usa_customers) == 2

    def test_list_recent_customers_by_country_empty_service(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([], f)
            temp_file_path = f.name
        
        try:
            service = CustomerService(temp_file_path)
            customers = service.list_recent_customers_by_country("Brazil")
            assert len(customers) == 0
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_customer_attributes_after_loading(self, temp_customers_file):
        service = CustomerService(temp_customers_file)
        
        for customer in service.customers:
            assert isinstance(customer.id, int)
            assert isinstance(customer.name, str)
            assert isinstance(customer.country, str)
            assert isinstance(customer.joined_at, datetime)

    def test_load_customers_with_malformed_data(self):
        malformed_data = [
            {
                "id": 1,
                "name": "John Doe",
                "country": "USA",
                "joinedAt": "2024-01-15T10:30:00Z"
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "country": "USA"
                # missing joinedAt
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(malformed_data, f)
            temp_file_path = f.name
        
        try:
            with pytest.raises(Exception):
                CustomerService(temp_file_path)
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_list_recent_customers_by_country_multiple_countries(self, temp_customers_file):
        service = CustomerService(temp_customers_file)
        
        usa_customers = service.list_recent_customers_by_country("USA")
        france_customers = service.list_recent_customers_by_country("France")
        japan_customers = service.list_recent_customers_by_country("Japan")
        
        assert len(usa_customers) == 2
        assert len(france_customers) == 2
        assert len(japan_customers) == 1
        

        assert france_customers[0].name == "Sophie Martin"
        assert france_customers[1].name == "Pierre Dupont"

    def test_list_recent_customers_by_country_zero_limit(self, temp_customers_file):
        service = CustomerService(temp_customers_file)
        
        customers = service.list_recent_customers_by_country("Brazil", limit=0)
        assert len(customers) == 0

    def test_list_recent_customers_by_country_negative_limit(self, temp_customers_file):
        service = CustomerService(temp_customers_file)
        
        customers = service.list_recent_customers_by_country("Brazil", limit=-1)
        assert len(customers) == 2
        assert customers[0].name == "Ronaldinho Gaucho"
        assert customers[1].name == "Maria Silva" 