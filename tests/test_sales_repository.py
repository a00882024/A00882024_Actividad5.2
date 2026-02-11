"""Tests for SaleRecord and SalesRepository."""

import json
import pytest

from src.sales_repository import SaleRecord, SalesRepository


@pytest.fixture
def sample_sales_data():
    return [
        {"SALE_ID": 1, "SALE_Date": "01/01/24", "Product": "Apple",
         "Quantity": 3},
        {"SALE_ID": 2, "SALE_Date": "01/01/24", "Product": "Bread",
         "Quantity": 2},
    ]


@pytest.fixture
def sample_sales_file(tmp_path, sample_sales_data):
    filepath = tmp_path / "sales.json"
    filepath.write_text(json.dumps(sample_sales_data))
    return str(filepath)


class TestSaleRecord:
    def test_attribute_access(self):
        record = SaleRecord(
            {"SALE_ID": 5, "SALE_Date": "02/03/24", "Product": "Milk",
             "Quantity": 10}
        )
        assert record.SALE_ID == 5
        assert record.SALE_Date == "02/03/24"
        assert record.Product == "Milk"
        assert record.Quantity == 10


class TestSalesRepository:
    def test_iteration(self, sample_sales_data):
        repo = SalesRepository(sample_sales_data)
        products = [sale.Product for sale in repo]
        assert products == ["Apple", "Bread"]

    def test_len(self, sample_sales_data):
        repo = SalesRepository(sample_sales_data)
        assert len(repo) == 2

    def test_empty_list(self):
        repo = SalesRepository([])
        assert len(repo) == 0
        assert list(repo) == []

    def test_from_json(self, sample_sales_file):
        repo = SalesRepository.from_json(sample_sales_file)
        assert len(repo) == 2
        first = next(iter(repo))
        assert first.Product == "Apple"
