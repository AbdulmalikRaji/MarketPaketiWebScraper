class ProductListItemUrlsDto(object):

    def __init__(self, list_url="",product_urls=[], isScraped=False):
        self.list_url = list_url
        self.product_urls = product_urls
        self.isScraped = isScraped

