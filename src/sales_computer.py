"""Business logic for computing sales totals."""

from src.product_repository import ProductRepository
from src.sales_repository import SalesRepository


class SalesComputer:
    """Computes per-product and grand totals from sales and catalogue data."""

    def __init__(self, products: ProductRepository, sales: SalesRepository):
        self._products = products
        self._sales = sales

    def compute(self) -> dict:
        """
        Return {
            "per_product": {title: total, ...},
            "grand_total": float
        }.
        """
        per_product: dict[str, float] = {}

        for sale in self._sales:
            product = self._products.get(sale.Product)
            if product is None:
                continue
            revenue = product["price"] * sale.Quantity
            per_product[sale.Product] = (
                per_product.get(sale.Product, 0)
                + revenue
            )

        return {
            "per_product": per_product,
            "grand_total": sum(per_product.values()),
        }
