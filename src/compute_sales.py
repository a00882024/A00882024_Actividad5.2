"""Compute total sales from a product catalogue and a sales record."""

import sys

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

    products = ProductRepository.from_json(product_file)
    sales = SalesRepository.from_json(sales_file)

    print(f"Products loaded: {len(products)}")
    print(f"Sales loaded: {len(sales)}")

    computer = SalesComputer(products, sales)
    result = computer.compute()

    for title, total in result["per_product"].items():
        print(f"  {title}: ${total:,.2f}")
    print(f"Grand total: ${result['grand_total']:,.2f}")

    computer.save_to_file(result, "results/SalesResults.txt")


if __name__ == "__main__":
    main()
