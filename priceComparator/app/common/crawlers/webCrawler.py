import json
from abc import abstractmethod

import requests
from bs4 import BeautifulSoup, element, ResultSet
from urllib3.exceptions import HTTPError

from ...interfaces.productScraperInterface import ProductScraperInterface
from ...models import Product


class WebCrawler(ProductScraperInterface):
    url: str
    retry: int = 3
    jsoup: BeautifulSoup
    json: json

    def connect(self, url):
        page = requests.get(url)
        page.raise_for_status()
        self.jsoup = BeautifulSoup(page.content, 'html.parser')

    def connect_wit_retries(self, url):
        i = 0
        while i < self.retry:
            try:
                self.connect(url)
                break
            except HTTPError as e:
                print(e)
                i += 1

    def search_products(self, search):
        search = search.replace(" ", "+")
        self.connect_wit_retries(self.url.format(search))
        elements = self.get_product_elements()
        products = []
        for product_element in elements:
            product = Product()
            product.name = self.get_name(product_element)
            product.sku = self.get_sku(product_element)
            product.status = self.get_status(product_element)
            product.brand = self.get_brand(product_element)
            product.model = self.get_model(product_element)
            product.image = self.get_image(product_element)
            product.offer_price = self.get_offer_price(product_element)
            product.normal_price = self.get_normal_price(product_element)
            product.url = self.get_url(product_element)
            product.price = min(product.offer_price, product.normal_price)
            products.append(product)

        return products

    @abstractmethod
    def get_product_elements(self) -> ResultSet:
        pass

    @abstractmethod
    def get_name(self, product_element: element) -> str:
        pass

    @abstractmethod
    def get_sku(self, product_element: element) -> str:
        pass

    @abstractmethod
    def get_brand(self, product_element: element) -> str:
        pass

    @abstractmethod
    def get_normal_price(self, product_element: element) -> float:
        pass

    @abstractmethod
    def get_offer_price(self, product_element: element) -> float:
        pass

    @abstractmethod
    def get_image(self, product_element: element) -> str:
        pass

    @abstractmethod
    def get_status(self, product_element: element) -> int:
        pass

    @abstractmethod
    def get_url(self, product_element: element) -> str:
        pass

    @abstractmethod
    def get_model(self, product_element: element) -> str:
        pass
