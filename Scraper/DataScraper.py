#from this import s
from bs4 import BeautifulSoup
import requests
import re
import time
from datetime import datetime
import pandas as pd
from Models import ProductUrlsDto,ProductDetailDto,ProductListItemUrlsDto
from Logger import LogManager as LM
import concurrent.futures
from Props import StaticProps as Props
import json

#ToDo: remember to get this url from that url file
#html_text=requests.get('https://www.altunbilekler.com/sitemap.xml')

class DataScraper(object):

    @staticmethod
    def ScrapeSitemapProductList(html_text):
        dataToReturn = ProductUrlsDto.ProductUrlsDto();
        dataToReturn.product_urls = [];
        dataToReturn.isScraped = 0;

        try:
            ##TODO check results
            reg='https:\/\/www\.marketpaketi\.com\.tr\/sitemaps\/sitemap\-product\-[0-9]+\.xml'
            sitemap_links=re.findall(reg,html_text)

            for link in sitemap_links:
                dataToReturn.product_urls.append(link)
            

            #Iterating over sitemap links
            #for link in sitemap_links:
            #    products_text=requests.get(link).text

            #    soup=BeautifulSoup(products_text,'lxml')

            #    #Get product links of all the categories
            #    product_links=soup.find_all('xhtml:link',hreflang="tr")

            #    for product_link in product_links:
            #        product_link=product_link.get('href')
            #        dataToReturn.product_urls.append(product_link)

        except Exception as e:
            LM.LogManager.logMessage("DataScraper-ScrapeSitemapProductList-" + str(e), LM.LogType.ERROR);

        if(len(dataToReturn.product_urls)>0):
            dataToReturn.isScraped = 1;
        return dataToReturn;

    @staticmethod
    def ScrapeProductListItemUrls(mainCategories):
        mainCatResultsToReturn = [];
        try:
            for link in mainCategories:
                newMarketResult = ProductListItemUrlsDto.ProductListItemUrlsDto();
                newMarketResult.list_url = link.item_url;
                newMarketResult.isScraped = False;
                newMarketResult.product_urls=[]

                products_text=link.html_detail
                
                reg1 = '<loc>.*<\/loc>'

                #Get product links of all the categories
                product_links=re.findall(reg1, products_text)
                urls = map(lambda x:x.replace("<loc>", "").replace("</loc>", ""), product_links)
                product_links = list(urls)
                for product_link in product_links:
                    newMarketResult.product_urls.append(product_link);

                newMarketResult.isScraped=True;
                mainCatResultsToReturn.append(newMarketResult);

        except Exception as e:
            LM.LogManager.logMessage("DataScraper-ScrapeMainCategories-" + str(e), LM.LogType.EXCEPTION);

        return mainCatResultsToReturn;

    def ScrapeSingleProductDetail(product):
        #Get the html and scripts details of a product
        newInfo = ProductDetailDto.ProductDetailDto()
        newInfo.product_url = product.item_url
        newInfo.brandList = []
        newInfo.catList = []

        try:
            soup = BeautifulSoup(product.html_text, 'lxml');
            product_info = soup.find('div', class_='container').find_all('script')
            categories = []
            category = json.loads(product_info[0].text)
            product = json.loads(product_info[1].text)
            old_price = soup.find('div', class_='eski_fiyat')


            newInfo.product_barcode=product['sku'][3:]
            newInfo.product_stockcode=product['sku']
            newInfo.product_name=product['name']
            newInfo.product_unit = ""
            newInfo.brandList.append(product['brand']['name'])
            newInfo.product_img_url =  product['image']

            newInfo.product_price=product['offers']['price']
            newInfo.product_old_price= old_price

            for items in category['itemListElement']:
                categories.append(items['item']['name'])

            while len(categories)<7:
                categories.append('')

            newInfo.catList=categories
            newInfo.isScraped = True

        except Exception as e:
            LM.LogManager.logMessage("DataScraper-ScrapeSinglePageForProducts-URL = " + product.item_url + str(e), LM.LogType.EXCEPTION);

        return newInfo

    #MultiThreading Functions
    @staticmethod
    def ScrapeProductDetails(productDetails):
        records=[]
        results = []

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers= Props.ScrapingWorkProps.threadPoolExecutorMaxPoolSize) as executor:
                for items in executor.map(DataScraper.ScrapeSingleProductDetail, productDetails):
                    results.append(items)
        except Exception as e:
            LM.LogManager.logMessage("DataScraper-ScrapeProductDetails-" + str(e), LM.LogType.ERROR);

        return results;
