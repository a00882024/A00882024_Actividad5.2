"""Repository for sales record data."""

import json


class SaleRecord:
    """Thin wrapper around a sale dict providing attribute access."""

    def __init__(self, data):
        self._data = data

    @property
    def SALE_ID(self):
        return self._data["SALE_ID"]

    @property
    def SALE_Date(self):
        return self._data["SALE_Date"]

    @property
    def Product(self):
        return self._data["Product"]

    @property
    def Quantity(self):
        return self._data["Quantity"]


class SalesRepository:
    """Iterable collection of SaleRecord objects."""

    def __init__(self, sale_list):
        self._records = []
        for i, s in enumerate(sale_list):
            if "Product" not in s:
                print(f'Skipping sale at index {i} — missing "Product"')
                continue
            if "Quantity" not in s:
                print(f'Skipping sale at index {i} — missing "Quantity"')
                continue
            if not isinstance(s["Quantity"], (int, float)):
                print(f'Skipping sale at index {i} — "Quantity" not numeric')
                continue
            self._records.append(SaleRecord(s))

    def __iter__(self):
        return iter(self._records)

    def __len__(self):
        return len(self._records)

    @classmethod
    def from_json(cls, filepath):
        """Load a sales JSON file and return a SalesRepository."""
        with open(filepath, "r", encoding="utf-8") as f:
            return cls(json.load(f))
