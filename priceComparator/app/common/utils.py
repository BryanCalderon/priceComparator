import datetime
from urllib.error import HTTPError

import requests

URL = 'https://trm-colombia.vercel.app/?date={}'

dollar_today = None


def get_min_price(price_1, price_2):
    if price_1 is not None and price_2 is not None:
        return min(price_1, price_2)
    elif price_1 is not None:
        return price_1
    elif price_2 is not None:
        return price_2

    return None


def get_trm():
    global dollar_today
    if not dollar_today:
        url = URL.format(datetime.date.today())
        i = 0
        while i < 3:
            try:
                print("Requesting to: {}".format(url))
                page = requests.get(url)
                page.raise_for_status()
                json = page.json()
                dollar_today = json.get('data').get('value')
                break
            except HTTPError as e:
                print(e)
                i += 1

    return dollar_today
