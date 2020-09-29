from importlib import import_module


def get_product_page_store(store_class_name):
    mod = import_module('priceComparator.app.common.crawlers.{}'.format(store_class_name))
    class_ = getattr(mod, store_class_name)
    return class_
