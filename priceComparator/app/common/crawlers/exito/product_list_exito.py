import json

from ... import utils
from ...ProductListWebCrawlerJson import ProductListWebCrawlerJson


class product_list_exito(ProductListWebCrawlerJson):
    url = "https://www.exito.com/api/catalog_system/pub/products/search/?ft={}&_from=0&_to=30&sc=2&O=OrderByScoreDESC"

    def get_product_elements(self):
        return self.json

    def get_name(self, json_product: json):
        return json_product.get('productName')

    def get_sku(self, json_product: json) -> str:
        return json_product.get('productId')

    def get_brand(self, json_product: json) -> str:
        return json_product.get('brand')

    def get_normal_price(self, json_product: json) -> float:
        normal_price = self.get_value_seller(json_product, 'ListPrice')
        if normal_price and normal_price < 4000:
            trm = utils.get_trm()
            normal_price = float("{:.2f}".format(trm * normal_price))
        return normal_price

    def get_offer_price(self, json_product: json) -> float:
        offer_price = self.get_value_seller(json_product, 'Price')
        if offer_price and offer_price < 4000:
            trm = utils.get_trm()
            offer_price = float("{:.2f}".format(trm * offer_price))
        return offer_price

    def get_image(self, json_product: json) -> str:
        return self.get_image_from_json(json_product)

    def get_status(self, json_product: json) -> int:
        cant = self.get_value_seller(json_product, 'AvailableQuantity')
        return cant is not None and cant > 0

    def get_url(self, json_product: json) -> str:
        return json_product.get('link')

    def get_model(self, json_product: json) -> str:
        return None

    def get_value_seller(self, json_product, type_price):
        item = self.get_item_product(json_product)
        price = None
        if item:
            sellers = item['sellers']
            for seller in sellers:
                if seller['sellerDefault']:
                    price = seller['commertialOffer'][type_price]
        return price

    def get_image_from_json(self, json_product):
        item = self.get_item_product(json_product)
        if item:
            return item['images'][0]['imageUrl']

    @staticmethod
    def get_item_product(json_product):
        items = json_product['items']
        if len(items) > 0:
            return items[0]
