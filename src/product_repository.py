"""Repository for product catalogue data."""

import json


class ProductRepository:
    """Stores products indexed by title for fast lookup."""

    def __init__(self, product_list):
        self._products = {}
        for i, p in enumerate(product_list):
            if "title" not in p:
                print(f'Skipping product at index {i} — missing "title"')
                continue
            if "price" not in p:
                print(f'Skipping product at index {i} — missing "price"')
                continue
            if not isinstance(p["price"], (int, float)):
                print(f'Skipping product at index {i} — "price" not numeric')
                continue
            self._products[p["title"]] = p

    def get(self, title):
        """Return the product dict for *title*, or None if not found."""
        return self._products.get(title)

    def __len__(self):
        return len(self._products)

    @classmethod
    def from_json(cls, filepath):
        """Load a product list JSON file and return a ProductRepository."""
        with open(filepath, "r", encoding="utf-8") as f:
            return cls(json.load(f))
