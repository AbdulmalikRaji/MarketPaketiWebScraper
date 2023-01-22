
class ProductDetailDto(object):
    def __init__(self,
                 product_url="",
                 product_name="",
                 product_price="",
                 product_old_price = "",
                 product_unit="",
                 product_img_url="",
                 product_barcode="",
                 product_stockcode="",
                 isScraped = False,
                 catList=[],
                 brandList=[]):

        self.product_url = product_url
        self.product_name = product_name
        self.product_barcode = product_barcode
        self.product_stockcode = product_stockcode
        self.brandList = brandList
        self.product_unit = product_unit
        self.product_img_url = product_img_url
        self.product_price = product_price
        self.product_old_price = product_old_price
        self.catList = catList
        self.isScraped = isScraped

