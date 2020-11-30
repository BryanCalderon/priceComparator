from ..models import Product


class ProductScraperInterface:

    def connect(self, url: str):
        pass

    def connect_wit_retries(self, url: str):
        pass

    def extract_product(self, product: Product) -> Product:
        pass
