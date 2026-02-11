"""Tests for compute_sales module."""

import json
import pytest
from unittest.mock import patch

from src.compute_sales import main


# --- Fixtures ---

@pytest.fixture
def sample_catalogue(tmp_path):
    """Create a temporary product catalogue JSON file."""
    data = [
        {"title": "Apple", "price": 1.50},
        {"title": "Bread", "price": 2.00},
        {"title": "Milk", "price": 3.25},
    ]
    filepath = tmp_path / "products.json"
    filepath.write_text(json.dumps(data))
    return str(filepath)


@pytest.fixture
def sample_sales(tmp_path):
    """Create a temporary sales JSON file."""
    data = [
        {"SALE_ID": 1, "SALE_Date": "01/01/24", "Product": "Apple",
         "Quantity": 3},
        {"SALE_ID": 1, "SALE_Date": "01/01/24", "Product": "Bread",
         "Quantity": 2},
    ]
    filepath = tmp_path / "sales.json"
    filepath.write_text(json.dumps(data))
    return str(filepath)


# --- main() tests ---

class TestMain:
    def test_wrong_arg_count(self):
        with patch("sys.argv", ["compute_sales.py"]):
            with pytest.raises(SystemExit):
                main()

    def test_loads_files(self, sample_catalogue, sample_sales, capsys):
        with patch("sys.argv",
                   ["compute_sales.py", sample_catalogue, sample_sales]):
            main()
        captured = capsys.readouterr()
        assert "Products loaded: 3" in captured.out
        assert "Sales loaded: 2" in captured.out
