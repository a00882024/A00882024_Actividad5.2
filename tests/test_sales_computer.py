"""Tests for SalesComputer."""
# pylint: disable=missing-function-docstring,missing-class-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=use-implicit-booleaness-not-comparison
# pylint: disable=protected-access

import pytest

from src.product_repository import ProductRepository
from src.sales_repository import SalesRepository
from src.sales_computer import SalesComputer


@pytest.fixture
def two_products():
    return ProductRepository([
        {"title": "Apple", "price": 1.50},
        {"title": "Bread", "price": 2.00},
    ])


@pytest.fixture
def two_sales():
    return SalesRepository([
        {"SALE_ID": 1, "SALE_Date": "01/01/24", "Product": "Apple",
         "Quantity": 3},
        {"SALE_ID": 2, "SALE_Date": "01/01/24", "Product": "Bread",
         "Quantity": 2},
    ])


class TestSalesComputer:
    def test_basic_computation(self, two_products, two_sales):
        result = SalesComputer(two_products, two_sales).compute()
        assert result["per_product"]["Apple"] == pytest.approx(4.50)
        assert result["per_product"]["Bread"] == pytest.approx(4.00)
        assert result["grand_total"] == pytest.approx(8.50)

    def test_unknown_product_skipped(self, two_products):
        sales = SalesRepository([
            {"SALE_ID": 1, "SALE_Date": "01/01/24", "Product": "Apple",
             "Quantity": 2},
            {"SALE_ID": 2, "SALE_Date": "01/01/24", "Product": "Ghost",
             "Quantity": 5},
        ])
        result = SalesComputer(two_products, sales).compute()
        assert "Ghost" not in result["per_product"]
        assert result["per_product"]["Apple"] == pytest.approx(3.00)
        assert result["grand_total"] == pytest.approx(3.00)

    def test_multiple_sales_same_product(self, two_products):
        sales = SalesRepository([
            {"SALE_ID": 1, "SALE_Date": "01/01/24", "Product": "Apple",
             "Quantity": 2},
            {"SALE_ID": 2, "SALE_Date": "02/01/24", "Product": "Apple",
             "Quantity": 3},
        ])
        result = SalesComputer(two_products, sales).compute()
        assert result["per_product"]["Apple"] == pytest.approx(7.50)
        assert result["grand_total"] == pytest.approx(7.50)

    def test_empty_sales(self, two_products):
        sales = SalesRepository([])
        result = SalesComputer(two_products, sales).compute()
        assert result["per_product"] == {}
        assert result["grand_total"] == 0

    def test_empty_products(self, two_sales):
        products = ProductRepository([])
        result = SalesComputer(products, two_sales).compute()
        assert result["per_product"] == {}
        assert result["grand_total"] == 0

    def test_type_error_in_compute_is_skipped(self, capsys):
        products = ProductRepository([
            {"title": "Apple", "price": 1.50},
        ])
        sales = SalesRepository([
            {"SALE_ID": 1, "SALE_Date": "01/01/24", "Product": "Apple",
             "Quantity": 3},
        ])
        # Corrupt the stored price to trigger a TypeError during multiply
        products._products["Apple"]["price"] = None
        result = SalesComputer(products, sales).compute()
        assert "Apple" not in result["per_product"]
        assert result["grand_total"] == 0
        output = capsys.readouterr().out
        assert "Skipping sale" in output

    def test_save_to_file(self, two_products, two_sales, tmp_path):
        computer = SalesComputer(two_products, two_sales)
        result = computer.compute()
        out = tmp_path / "SalesResults.txt"
        computer.save_to_file(result, str(out), 0.123456)

        lines = out.read_text().splitlines()
        assert lines[0] == "  Apple: $4.50"
        assert lines[1] == "  Bread: $4.00"
        assert lines[2] == "Grand total: $8.50"
        assert lines[3] == "Execution time: 0.123456 seconds"
