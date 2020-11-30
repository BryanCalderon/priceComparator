from ... import utils
from ...ProductPageWebCrawlerJson import ProductPageWebCrawlerJson

URL_PRODUCT_PAGE = "https://www.exito.com/api/catalog_system/pub/products/search?fq=skuId:{}"


class product_page_exito(ProductPageWebCrawlerJson):

    def set_url(self, product):
        return URL_PRODUCT_PAGE.format(product.sku)

    def get_product_element(self):
        return self.json

    def get_name(self):
        return self.json.get('productName')

    def get_sku(self) -> str:
        return self.json.get('productId')

    def get_brand(self) -> str:
        return self.json.get('brand')

    def get_normal_price(self) -> float:
        normal_price: float = self.get_value_seller(self.json, 'ListPrice')
        if normal_price and normal_price < 4000:
            trm = utils.get_trm()
            normal_price = float("{:.2f}".format(trm * normal_price))
        return normal_price

    def get_offer_price(self) -> float:
        offer_price = self.get_value_seller(self.json, 'Price')
        if offer_price and offer_price < 4000:
            trm = utils.get_trm()
            offer_price = float("{:.2f}".format(trm * offer_price))
        return offer_price

    def get_image(self) -> str:
        return self.get_image_from_json(self.json)

    def get_status(self) -> int:
        cant = self.get_value_seller(self.json, 'AvailableQuantity')
        return cant is not None and cant > 0

    def get_url(self) -> str:
        return self.json.get('link')

    def get_model(self) -> str:
        model = self.json.get('Referencia')
        if isinstance(model, list) and len(model) > 0:
            model = model[0]
        return model

    def get_value_seller(self, json_product, type_price):
        price = None
        seller = self.get_seller(json_product)
        if seller:
            price = seller["commertialOffer"][type_price]

        return price

    def get_seller(self, json_product):
        item = self.get_item_product(json_product)
        result = None
        if item:
            sellers = item['sellers']
            result = [seller for seller in sellers if seller['sellerDefault']]
        return result[0] if result else None

    def get_image_from_json(self, json_product):
        item = self.get_item_product(json_product)
        if item:
            return item['images'][0]['imageUrl']

    @staticmethod
    def get_item_product(json_product):
        items = json_product['items']
        if len(items) > 0:
            return items[0]
