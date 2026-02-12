"""Compute total sales from a product catalogue and a sales record."""

import json
import sys
import time

from src.product_repository import ProductRepository
from src.sales_repository import SalesRepository
from src.sales_computer import SalesComputer


def main():
    if len(sys.argv) != 3:
        print("Usage: python -m src.compute_sales <product_list.json>"
              " <sales.json>")
        sys.exit(1)

    product_file = sys.argv[1]
    sales_file = sys.argv[2]

    try:
        products = ProductRepository.from_json(product_file)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"Error loading product file: {exc}")
        sys.exit(1)

    try:
        sales = SalesRepository.from_json(sales_file)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"Error loading sales file: {exc}")
        sys.exit(1)

    print(f"Products loaded: {len(products)}")
    print(f"Sales loaded: {len(sales)}")

    computer = SalesComputer(products, sales)

    start = time.perf_counter()
    result = computer.compute()
    elapsed = time.perf_counter() - start

    for title, total in result["per_product"].items():
        print(f"  {title}: ${total:,.2f}")
    print(f"Grand total: ${result['grand_total']:,.2f}")
    print(f"Execution time: {elapsed:.6f} seconds")

    computer.save_to_file(result, "results/SalesResults.txt", elapsed)


if __name__ == "__main__":
    main()
