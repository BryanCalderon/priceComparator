import re

from ...productPageWebCrawler import ProductPageWebCrawler


class product_page_alkosto(ProductPageWebCrawler):

    def set_url(self, product):
        return product.url

    def get_product_element(self):
        return self.jsoup.select_one(".product-name")

    def get_name(self):
        name_element = self.jsoup.select_one(".product-name h1")
        name = None
        if name_element:
            name = name_element.string
        return name

    def get_sku(self) -> str:
        return self.jsoup.select_one("span[itemprop=sku]").string

    def get_brand(self) -> str:
        element = self.jsoup.select_one("span[itemprop=brand]")
        brand = None
        if element:
            brand = element.string
        return brand

    def get_normal_price(self) -> float:
        normal_price = None
        price_str = self.jsoup.select_one(".product-main-info .price-box .old-price span.price-old")
        if price_str is None:
            price_str = self.jsoup.select_one(".product-main-info .price-box .regular-price span[itemprop=price]")

        if price_str:
            normal_price = float(self.parse_price(price_str.text))

        return normal_price

    def get_offer_price(self) -> float:
        offer_price = None
        price_str = self.jsoup.select_one(".product-main-info .price-box p.special-price span[itemprop=price]")
        if price_str:
            offer_price = float(self.parse_price(price_str.text))
        return offer_price

    def get_image(self) -> str:
        image = self.jsoup.find("meta[property=og:image]")
        value = None
        if image:
            value = image['content']
        return value

    def get_status(self) -> int:
        button = self.jsoup.select_one(".product-essential .add-to-cart")
        return button is not None

    def get_url(self) -> str:
        url = self.jsoup.find("meta[property=og:url]")
        value = None
        if url:
            value = url['content']
        return value

    def get_model(self) -> str:
        items = self.jsoup.select_one("#product-attribute-specs-table").select("td li")
        model = None

        for item in items:
            if item.text.__contains__("Referencia"):
                model = item.text.split(":")[1].strip()

        return model

    @staticmethod
    def parse_price(price):
        price = re.search('[\d\.?\,]+', price).group()
        return price.replace(".", "")
