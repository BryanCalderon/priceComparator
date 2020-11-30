from importlib import import_module

from soupsieve.util import lower


def get_product_page_class(store_name):
    store_name = lower(store_name)
    class_name = 'product_page_{}'.format(store_name)
    return import_class(store_name, class_name)


def get_product_list_class(store_name):
    store_name = lower(store_name)
    class_name = 'product_list_{}'.format(lower(store_name))
    return import_class(store_name, class_name)


def import_class(store_name, class_name):
    mod = import_module('priceComparator.app.common.crawlers.{}.{}'.format(store_name, class_name))
    class_ = getattr(mod, class_name)
    return class_
