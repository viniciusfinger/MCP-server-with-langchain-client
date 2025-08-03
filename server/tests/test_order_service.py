import pytest
import json
import tempfile
import os
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch, mock_open
from service.order_service import OrderService
from model.order import Order


class TestOrderService:

    @pytest.fixture
    def sample_orders_data(self):
        return [
            {
                "id": 1,
                "customerId": 1,
                "customerName": "Vinicius Finger",
                "date": "2025-03-05T14:30:00Z",
                "amount": 350.25
            },
            {
                "id": 2,
                "customerId": 1,
                "customerName": "Vinicius Finger",
                "date": "2025-03-18T09:45:00Z",
                "amount": 420.50
            },
            {
                "id": 3,
                "customerId": 2,
                "customerName": "Cauê Finger",
                "date": "2025-02-15T11:15:00Z",
                "amount": 390.30
            },
            {
                "id": 4,
                "customerId": 2,
                "customerName": "Cauê Finger",
                "date": "2025-04-02T13:50:00Z",
                "amount": 485.20
            },
            {
                "id": 5,
                "customerId": 1,
                "customerName": "Vinicius Finger",
                "date": "2025-05-12T16:20:00Z",
                "amount": 275.75
            }
        ]

    @pytest.fixture
    def temp_orders_file(self, sample_orders_data):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sample_orders_data, f)
            temp_file_path = f.name
        
        yield temp_file_path
        
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

    def test_init_with_default_file_path(self):
        with patch('builtins.open', mock_open(read_data='[]')):
            service = OrderService()
            assert service.orders == []

    def test_init_with_custom_file_path(self):
        custom_path = "custom/path/orders.json"
        with patch('builtins.open', mock_open(read_data='[]')):
            service = OrderService(custom_path)
            assert service.orders == []

    def test_load_orders_success(self, temp_orders_file):
        service = OrderService(temp_orders_file)
        
        assert len(service.orders) == 5
        assert all(isinstance(order, Order) for order in service.orders)
        
        first_order = service.orders[0]
        assert first_order.id == 1
        assert first_order.customer_id == 1
        assert first_order.customer_name == "Vinicius Finger"
        assert first_order.amount == Decimal('350.25')

    def test_load_orders_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            OrderService("arquivo_inexistente.json")

    def test_load_orders_invalid_json(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": json}')
            temp_file_path = f.name
        
        try:
            with pytest.raises(json.JSONDecodeError):
                OrderService(temp_file_path)
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_get_order_count_by_customer_and_month_exact_match(self, temp_orders_file):
        service = OrderService(temp_orders_file)
        
        count = service.get_order_count_by_customer_and_month("Vinicius Finger", "2025-03")
        assert count == 2

    def test_get_order_count_by_customer_and_month_no_match(self, temp_orders_file):
        service = OrderService(temp_orders_file)
        
        count = service.get_order_count_by_customer_and_month("Cliente Inexistente", "2025-03")
        assert count == 0
        
        count = service.get_order_count_by_customer_and_month("Vinicius Finger", "2025-12")
        assert count == 0

    def test_get_order_count_by_customer_and_month_case_sensitive(self, temp_orders_file):
        service = OrderService(temp_orders_file)
        
        count = service.get_order_count_by_customer_and_month("joão silva", "2025-03")
        assert count == 0

    def test_get_order_count_by_customer_and_month_different_months(self, temp_orders_file):
        service = OrderService(temp_orders_file)
        
        count = service.get_order_count_by_customer_and_month("Vinicius Finger", "2025-02")
        assert count == 0
        
        count = service.get_order_count_by_customer_and_month("Vinicius Finger", "2025-05")
        assert count == 1
        
        count = service.get_order_count_by_customer_and_month("Cauê Finger", "2025-02")
        assert count == 1

    def test_get_order_count_by_customer_and_month_empty_service(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([], f)
            temp_file_path = f.name
        
        try:
            service = OrderService(temp_file_path)
            count = service.get_order_count_by_customer_and_month("João Silva", "2025-03")
            assert count == 0
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_get_order_count_by_customer_and_month_invalid_date_format(self, temp_orders_file):
        service = OrderService(temp_orders_file)
        
        count = service.get_order_count_by_customer_and_month("João Silva", "2025-3")
        assert count == 0
        
        count = service.get_order_count_by_customer_and_month("João Silva", "2025-03-01")
        assert count == 0

    def test_order_attributes_after_loading(self, temp_orders_file):
        service = OrderService(temp_orders_file)
        
        for order in service.orders:
            assert isinstance(order.id, int)
            assert isinstance(order.customer_id, int)
            assert isinstance(order.customer_name, str)
            assert isinstance(order.date, datetime)
            assert isinstance(order.amount, Decimal)

    def test_load_orders_with_malformed_data(self):
        malformed_data = [
            {
                "id": 1,
                "customerId": 1,
                "customerName": "João Silva",
                "date": "2025-03-05T14:30:00Z",
                "amount": 350.25
            },
            {
                "id": 2,
                "customerId": 1,
                "customerName": "João Silva",
                # missing date
                "amount": 420.50
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(malformed_data, f)
            temp_file_path = f.name
        
        try:
            with pytest.raises(Exception):
                OrderService(temp_file_path)
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path) 

    def test_calculate_aggregate_spending_for_customers_single_customer(self, temp_orders_file):
        service = OrderService(temp_orders_file)
        
        result = service.calculate_aggregate_spending_for_customers([1])
        
        assert len(result) == 1
        assert result[0]["customerId"] == 1
        assert result[0]["spend"] == 1046.50 #350.25 + 420.50 + 275.75 = 1046.50

    def test_calculate_aggregate_spending_for_customers_multiple_customers(self, temp_orders_file):
        service = OrderService(temp_orders_file)
        
        result = service.calculate_aggregate_spending_for_customers([1, 2])
        
        assert len(result) == 2
        
        customer_1_result = next(r for r in result if r["customerId"] == 1)
        assert customer_1_result["spend"] == 1046.50  # 350.25 + 420.50 + 275.75
        
        customer_2_result = next(r for r in result if r["customerId"] == 2)
        assert customer_2_result["spend"] == 875.50  # 390.30 + 485.20

    def test_calculate_aggregate_spending_for_customers_empty_list(self, temp_orders_file):
        service = OrderService(temp_orders_file)
        
        result = service.calculate_aggregate_spending_for_customers([])
        
        assert result == []

    def test_calculate_aggregate_spending_for_customers_nonexistent_customer(self, temp_orders_file):
        service = OrderService(temp_orders_file)
        
        result = service.calculate_aggregate_spending_for_customers([999])
        
        assert len(result) == 1
        assert result[0]["customerId"] == 999
        assert result[0]["spend"] == 0.0

    def test_calculate_aggregate_spending_for_customers_mixed_existent_nonexistent(self, temp_orders_file):
        service = OrderService(temp_orders_file)
        
        result = service.calculate_aggregate_spending_for_customers([1, 999, 2])
        
        assert len(result) == 3
        
        customer_1_result = next(r for r in result if r["customerId"] == 1)
        assert customer_1_result["spend"] == 1046.50
        
        customer_999_result = next(r for r in result if r["customerId"] == 999)
        assert customer_999_result["spend"] == 0.0
        
        customer_2_result = next(r for r in result if r["customerId"] == 2)
        assert customer_2_result["spend"] == 875.50

    def test_calculate_aggregate_spending_for_customers_duplicate_customer_ids(self, temp_orders_file):
        service = OrderService(temp_orders_file)
        
        result = service.calculate_aggregate_spending_for_customers([1, 1, 2])
        
        assert len(result) == 3
        
        customer_1_results = [r for r in result if r["customerId"] == 1]
        assert len(customer_1_results) == 2
        assert all(r["spend"] == 1046.50 for r in customer_1_results)
        
        customer_2_result = next(r for r in result if r["customerId"] == 2)
        assert customer_2_result["spend"] == 875.50

    def test_calculate_aggregate_spending_for_customers_empty_service(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([], f)
            temp_file_path = f.name
        
        try:
            service = OrderService(temp_file_path)
            result = service.calculate_aggregate_spending_for_customers([1, 2])
            
            assert len(result) == 2
            assert result[0]["customerId"] == 1
            assert result[0]["spend"] == 0.0
            assert result[1]["customerId"] == 2
            assert result[1]["spend"] == 0.0
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_calculate_aggregate_spending_for_customers_return_type(self, temp_orders_file):
        service = OrderService(temp_orders_file)
        
        result = service.calculate_aggregate_spending_for_customers([1])
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], dict)
        assert "customerId" in result[0]
        assert "spend" in result[0]
        assert isinstance(result[0]["customerId"], int)
        assert isinstance(result[0]["spend"], float)

    def test_calculate_aggregate_spending_for_customers_decimal_precision(self):
        precise_orders_data = [
            {
                "id": 1,
                "customerId": 1,
                "customerName": "Cliente Teste",
                "date": "2025-03-05T14:30:00Z",
                "amount": 100.123456
            },
            {
                "id": 2,
                "customerId": 1,
                "customerName": "Cliente Teste",
                "date": "2025-03-06T14:30:00Z",
                "amount": 200.987654
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(precise_orders_data, f)
            temp_file_path = f.name
        
        try:
            service = OrderService(temp_file_path)
            result = service.calculate_aggregate_spending_for_customers([1])
            
            assert len(result) == 1
            assert result[0]["customerId"] == 1

            assert result[0]["spend"] == 301.111110 # 100.123456 + 200.987654 = 301.111110
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_calculate_aggregate_spending_for_customers_order_preservation(self, temp_orders_file):
        service = OrderService(temp_orders_file)
        
        result = service.calculate_aggregate_spending_for_customers([2, 1, 999])
        
        assert len(result) == 3
        assert result[0]["customerId"] == 2
        assert result[1]["customerId"] == 1
        assert result[2]["customerId"] == 999

    def test_calculate_aggregate_spending_for_customers_zero_amount_orders(self):
        zero_amount_orders_data = [
            {
                "id": 1,
                "customerId": 1,
                "customerName": "Cliente Teste",
                "date": "2025-03-05T14:30:00Z",
                "amount": 0.0
            },
            {
                "id": 2,
                "customerId": 1,
                "customerName": "Cliente Teste",
                "date": "2025-03-06T14:30:00Z",
                "amount": 100.0
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(zero_amount_orders_data, f)
            temp_file_path = f.name
        
        try:
            service = OrderService(temp_file_path)
            result = service.calculate_aggregate_spending_for_customers([1])
            
            assert len(result) == 1
            assert result[0]["customerId"] == 1
            assert result[0]["spend"] == 100.0  # 0.0 + 100.0
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_calculate_aggregate_spending_for_customers_negative_amount_orders(self):
        negative_amount_orders_data = [
            {
                "id": 1,
                "customerId": 1,
                "customerName": "Cliente Teste",
                "date": "2025-03-05T14:30:00Z",
                "amount": -50.0
            },
            {
                "id": 2,
                "customerId": 1,
                "customerName": "Cliente Teste",
                "date": "2025-03-06T14:30:00Z",
                "amount": 100.0
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(negative_amount_orders_data, f)
            temp_file_path = f.name
        
        try:
            service = OrderService(temp_file_path)
            result = service.calculate_aggregate_spending_for_customers([1])
            
            assert len(result) == 1
            assert result[0]["customerId"] == 1
            assert result[0]["spend"] == 50.0  # -50.0 + 100.0
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_calculate_aggregate_spending_for_customers_large_numbers(self):
        large_amount_orders_data = [
            {
                "id": 1,
                "customerId": 1,
                "customerName": "Cliente Teste",
                "date": "2025-03-05T14:30:00Z",
                "amount": 999999.99
            },
            {
                "id": 2,
                "customerId": 1,
                "customerName": "Cliente Teste",
                "date": "2025-03-06T14:30:00Z",
                "amount": 1000000.01
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(large_amount_orders_data, f)
            temp_file_path = f.name
        
        try:
            service = OrderService(temp_file_path)
            result = service.calculate_aggregate_spending_for_customers([1])
            
            assert len(result) == 1
            assert result[0]["customerId"] == 1
            assert result[0]["spend"] == 2000000.0  # 999999.99 + 1000000.01
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path) 