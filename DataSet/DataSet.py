
class ProductUrl(object):
    productUrlColumns = ['product_url' , 'isScraped']
    productUrlListDtype = {
        "product_url":"object",
        "isScraped":"bool"
    }

class ProductDetail(object):
    productDetailColumns = ['product_url' , 'product_name',"product_code","product_unit","product_img_url","product_price","product_old_price",
                            "cat1","cat2","cat3","cat4","cat5","cat6","product_brand1","product_brand2","timestamp"]

    productDetailDtype = {
        "product_url":"object",
        "product_name":"object",
        "product_code":"object",
        "product_unit":"object",
        "product_img_url":"object",
        "product_price":"float",
        "product_old_price":"float",
        "cat1":"object",
        "cat2":"object",
        "cat3":"object",
        "cat4":"object",
        "cat5":"object",
        "cat6":"object",
        "product_brand1":"object",
        "product_brand2":"object",
        "timestamp":"object"
    }
