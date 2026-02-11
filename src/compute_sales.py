"""Compute total sales from a product catalogue and a sales record."""

import sys

from src.product_repository import ProductRepository
from src.sales_repository import SalesRepository


def main():
    if len(sys.argv) != 3:
        print("Usage: python -m src.compute_sales <product_list.json>"
              " <sales.json>")
        sys.exit(1)

    product_file = sys.argv[1]
    sales_file = sys.argv[2]

    products = ProductRepository.from_json(product_file)
    sales = SalesRepository.from_json(sales_file)

    print(f"Products loaded: {len(products)}")
    print(f"Sales loaded: {len(sales)}")


if __name__ == "__main__":
    main()
