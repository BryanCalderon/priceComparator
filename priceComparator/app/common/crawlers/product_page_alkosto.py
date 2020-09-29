import json
import re

from bs4 import element

from .webCrawler import WebCrawler


class product_page_alkosto(WebCrawler):
    url = "https://www.alkosto.com/salesperson/result/?q={}"

    def get_product_elements(self):
        return self.jsoup.select('li.salesperson-products-grid-item')

    def get_name(self, product_element: element):
        json_script = self.get_json_product(product_element)
        return json_script.get('name')

    def get_sku(self, product_element: element) -> str:
        json_script = self.get_json_product(product_element)
        return json_script.get('id')

    def get_brand(self, product_element: element) -> str:
        json_script = self.get_json_product(product_element)
        return json_script.get('brand')

    def get_normal_price(self, product_element: element) -> float:
        return float(self.parse_price(product_element.select_one(".price-box .old-price span.price-old").text))

    def get_offer_price(self, product_element: element) -> float:
        return float(self.parse_price(product_element.select_one(".price-box p.special-price span.price").text))

    def get_image(self, product_element: element) -> str:
        return product_element.find("img")['src']

    def get_status(self, product_element: element) -> int:
        button = product_element.select_one(
            "div.salesperson-category-products li.first div.actions div.add-to-cart button.btn-cart")
        return button is not None

    def get_url(self, product_element: element) -> str:
        return product_element.find("a")['href']

    def get_model(self, product_element: element) -> str:
        return None

    @staticmethod
    def get_json_product(product_element):
        script = product_element.select_one('script[type="text/javascript"]').string
        json_script = json.loads(script[script.find("{") - 1:script.find("}") + 1].replace("\'", '\"'))
        return json_script

    @staticmethod
    def parse_price(price):
        price = re.search('[\d\.?\,]+', price).group()
        return price.replace(".", "")
