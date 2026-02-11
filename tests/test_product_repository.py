"""Tests for ProductRepository."""

import json
import pytest

from src.product_repository import ProductRepository


@pytest.fixture
def sample_products():
    return [
        {"title": "Apple", "price": 1.50},
        {"title": "Bread", "price": 2.00},
        {"title": "Milk", "price": 3.25},
    ]


@pytest.fixture
def sample_product_file(tmp_path, sample_products):
    filepath = tmp_path / "products.json"
    filepath.write_text(json.dumps(sample_products))
    return str(filepath)


class TestProductRepository:
    def test_get_existing_product(self, sample_products):
        repo = ProductRepository(sample_products)
        product = repo.get("Bread")
        assert product is not None
        assert product["price"] == 2.00

    def test_get_unknown_title_returns_none(self, sample_products):
        repo = ProductRepository(sample_products)
        assert repo.get("Nonexistent") is None

    def test_len(self, sample_products):
        repo = ProductRepository(sample_products)
        assert len(repo) == 3

    def test_empty_list(self):
        repo = ProductRepository([])
        assert len(repo) == 0
        assert repo.get("anything") is None

    def test_from_json(self, sample_product_file):
        repo = ProductRepository.from_json(sample_product_file)
        assert len(repo) == 3
        assert repo.get("Apple")["price"] == 1.50
