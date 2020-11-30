import json
from abc import abstractmethod

import requests

from .productListWebCrawler import ProductListWebCrawler


class ProductListWebCrawlerJson(ProductListWebCrawler):

    def connect(self, url):
        page = requests.get(url)
        page.raise_for_status()
        self.json = page.json()

    @abstractmethod
    def get_product_elements(self) -> json:
        pass

    @abstractmethod
    def get_name(self, product_element: json) -> str:
        pass

    @abstractmethod
    def get_sku(self, product_element: json) -> str:
        pass

    @abstractmethod
    def get_brand(self, product_element: json) -> str:
        pass

    @abstractmethod
    def get_normal_price(self, product_element: json) -> float:
        pass

    @abstractmethod
    def get_offer_price(self, product_element: json) -> float:
        pass

    @abstractmethod
    def get_image(self, product_element: json) -> str:
        pass

    @abstractmethod
    def get_status(self, product_element: json) -> int:
        pass

    @abstractmethod
    def get_url(self, product_element: json) -> str:
        pass

    @abstractmethod
    def get_model(self, product_element: json) -> str:
        pass
