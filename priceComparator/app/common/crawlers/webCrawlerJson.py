import json
from abc import abstractmethod

import requests

from .webCrawler import WebCrawler


# URL_PRODUCT_PAGE = "/api/catalog_system/pub/products/search?fq=skuId:59870"
# URL_SEARCH = "/api/catalog_system/pub/products/search/?ft=tv%20lg%2055&_from=0&_to=9&sc=2&O=OrderByScoreDESC"
# URL_MENULINK = "/api/catalog_system/pub/products/search/?&fq=C%3a%2f679%2f687%2f776%2f&fq=C%3a%2f679%2f687%2f776%2f&sc="

class WebCrawlerJson(WebCrawler):

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
