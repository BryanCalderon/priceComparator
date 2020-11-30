import json

import requests

from .productPageWebCrawler import ProductPageWebCrawler


class ProductPageWebCrawlerJson(ProductPageWebCrawler):
    json: json

    def connect(self, url):
        page = requests.get(url)
        page.raise_for_status()
        self.json = page.json()
        if isinstance(self.json, list) and len(self.json) > 0:
            self.json = self.json[0]
