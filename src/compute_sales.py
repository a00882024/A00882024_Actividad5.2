"""Compute total sales from a product catalogue and a sales record."""

import json
import sys


def load_json(filepath):
    """Load and return parsed JSON from a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    if len(sys.argv) != 3:
        print("Usage: python -m src.compute_sales <product_list.json>"
              " <sales.json>")
        sys.exit(1)

    product_file = sys.argv[1]
    sales_file = sys.argv[2]

    product_catalogue = load_json(product_file)
    sales_records = load_json(sales_file)

    print(f"Products loaded: {len(product_catalogue)}")
    print(f"Sales loaded: {len(sales_records)}")


if __name__ == "__main__":
    main()
