class ProductListScraperInterface:

    def connect(self, url: str):
        pass

    def connect_wit_retries(self, url: str):
        pass

    def search_products(self, search: str) -> []:
        pass
