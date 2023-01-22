from decouple import config
from datetime import datetime

class APIRoutes(object):
    base_sitemap = 'https://www.altunbilekler.com/sitemap.xml'
    #base_product_list_sitemap_url = 'https://www.cagri.com/sitemap/products/'
    base_url = 'https://www.altunbilekler.com'

class EmailProps(object):
    base_email_account = config('userAccount',default='')
    base_email_password = config('password',default='')
    mail_receiver = config('mail_receiver',default='')
    mail_host = config('mail_host',default='')
    mail_port = int(config('mail_port',default=''))

class FilePathProps(object):
    processBasePath = 'ONPROCESS'
    uploadBasePath = 'UPLOADING'

    sitemapProductListPath = processBasePath + "/" + 'sitemap_product_list.xlsx' 
    productUrlListPath = processBasePath + "/" + 'product_url_list.xlsx'

    uploadingDestinationPath = r'D:\ScrapingData\ALTUNBILEKLER\UPLOADING';

    @staticmethod
    def GetMarketDataUploadingPath():
        return FilePathProps.uploadBasePath + "/" + "MarketData"+ datetime.today().strftime("%Y-%m-%d-%H-%M-%S") + '.xlsx';

    @staticmethod
    def GetProductDataUploadingPath():
        return FilePathProps.uploadBasePath + "/" + "ProductData"+ datetime.today().strftime("%Y-%m-%d-%H-%M-%S") + '.xlsx'

class ScrapingWorkProps(object):
    threadPoolExecutorMaxPoolSize = int(config('threadPoolExecutorMaxPoolSize',default=0))
    parallelWebRequestConcReqSize = int(config('parallelWebRequestConcReqSize',default=0))
    scrapingTotalTrialNo = int(config('scrapingTotalTrialNo',default=1)) #should be min 1
    scrapeProductListStatus = int(config('scrapeProductListStatus',default=1))
    scrapingDataSliceSize = int(config('scrapingDataSliceSize',default=1))

