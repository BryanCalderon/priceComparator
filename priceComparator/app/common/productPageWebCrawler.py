from abc import abstractmethod

import requests
from bs4 import BeautifulSoup, element
from urllib3.exceptions import HTTPError

from .utils import get_min_price
from ..interfaces.productScraperInterface import ProductScraperInterface


class ProductPageWebCrawler(ProductScraperInterface):
    retry: int = 3
    jsoup: BeautifulSoup
    element: element

    def connect(self, url):
        page = requests.get(url)
        page.raise_for_status()
        self.jsoup = BeautifulSoup(page.content, 'html.parser')

    def connect_wit_retries(self, url):
        i = 0
        while i < self.retry:
            try:
                print("Requesting to: {}".format(url))
                self.connect(url)
                break
            except HTTPError as e:
                print(e)
                i += 1

    def extract_product(self, product):
        self.connect_wit_retries(self.set_url(product))
        if self.get_product_element():
            product.status = self.get_status()

            name = self.get_name()
            if name:
                product.name = name

            sku = self.get_sku()
            if sku:
                product.sku = sku

            brand = self.get_brand()
            if brand:
                product.brand = brand

            model = self.get_model()
            if model:
                product.model = model

            image = self.get_image()
            if image:
                product.image = image

            offer_price = self.get_offer_price()
            if offer_price and offer_price > 0.0:
                product.offer_price = offer_price

            normal_price = self.get_normal_price()
            if normal_price and normal_price > 0.0:
                product.normal_price = normal_price

            url = self.get_url()
            if url:
                product.url = url

            product.price = get_min_price(product.offer_price, product.normal_price)

        return product.save()

    @abstractmethod
    def set_url(self, product):
        pass

    @abstractmethod
    def get_product_element(self) -> element:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_sku(self) -> str:
        pass

    @abstractmethod
    def get_brand(self) -> str:
        pass

    @abstractmethod
    def get_normal_price(self) -> float:
        pass

    @abstractmethod
    def get_offer_price(self) -> float:
        pass

    @abstractmethod
    def get_image(self) -> str:
        pass

    @abstractmethod
    def get_status(self) -> int:
        pass

    @abstractmethod
    def get_url(self) -> str:
        pass

    @abstractmethod
    def get_model(self) -> str:
        pass
