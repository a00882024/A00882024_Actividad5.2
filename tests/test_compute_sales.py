"""Tests for compute_sales module."""

import json
import pytest
from unittest.mock import patch

from src.compute_sales import load_json


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


# --- load_json tests ---

class TestLoadJson:
    def test_load_valid_json(self, sample_catalogue):
        data = load_json(sample_catalogue)
        assert len(data) == 3
        assert data[0]["title"] == "Apple"

    def test_load_invalid_json(self, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text("not valid json{{{")
        with pytest.raises(json.JSONDecodeError):
            load_json(str(bad))

    def test_load_sales_json(self, sample_sales):
        data = load_json(sample_sales)
        assert len(data) == 2
        assert data[0]["Product"] == "Apple"


# --- main() tests ---

class TestMain:
    def test_wrong_arg_count(self):
        with patch("sys.argv", ["compute_sales.py"]):
            with pytest.raises(SystemExit):
                from src.compute_sales import main
                main()

    def test_loads_files(self, sample_catalogue, sample_sales, capsys):
        with patch("sys.argv",
                   ["compute_sales.py", sample_catalogue, sample_sales]):
            from src.compute_sales import main
            main()
        captured = capsys.readouterr()
        assert "Products loaded: 3" in captured.out
        assert "Sales loaded: 2" in captured.out
