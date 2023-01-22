from DataRepository import DataServices
from Scraper import DataScraper 
import pandas as pd
from datetime import date,datetime
from Logger import LogManager as LM
from FileServices import FileServices
from Helpers import DataHelper as DataHelper
import xlsxwriter
from os.path import exists
import re
from Props import StaticProps as Props

class BusinessService(object):

     @staticmethod
     async def ScrapeSitemapProductLists():
         isSitemapProductListScraped = False;

         try:
             if(exists(Props.FilePathProps.sitemapProductListPath) == True):
                 sitemap_product_list_original_df = pd.read_excel(Props.FilePathProps.sitemapProductListPath, 0, header=0, engine='openpyxl')
                 count_row = sitemap_product_list_original_df.shape[0]
                 if(count_row!=None and count_row>0):
                     isSitemapProductListScraped = True;


             if(isSitemapProductListScraped==False):
                 sitemapHtmlResult = await DataServices.Requests.GetSitemapProductListsAsync();
                 dataToScrape = sitemapHtmlResult[0].html_detail;
                 
                 sitemap_product_lists_df = pd.DataFrame()
                 productListsResponse = DataScraper.DataScraper.ScrapeSitemapProductList(dataToScrape);

                 if(productListsResponse.isScraped==1):
                     for item in productListsResponse.product_urls:
                          excel_title = []
                          excel_value = []

                          excel_title.append("product_list_url")
                          excel_value.append(item)

                          excel_title.append("isScraped")
                          excel_value.append(False)

                          sitemap_product_lists_df = sitemap_product_lists_df.append(pd.Series(data=excel_value, index=excel_title), ignore_index=True)

                 ## SET IS SCRAPED TYPE TO INTEGER
                 #sitemap_product_lists_df['isScraped'] = sitemap_product_lists_df['isScraped'].astype(bool)
                 # CREATE EXCEL
                 sitemap_product_lists_df.to_excel(Props.FilePathProps.sitemapProductListPath, index=False)
                 scraped_list_count = sitemap_product_lists_df.shape[0]

                 if(scraped_list_count>0):
                     isSitemapProductListScraped = True;

         except Exception as e:
             LM.LogManager.logMessage("BusinessService-ScrapeSitemapProductLists-" + str(e), LM.LogType.ERROR);

         return isSitemapProductListScraped;

     @staticmethod
     async def ScrapeProductUrls():
         isSitemapProductListScraped = False;
         isProductUrlsScraped = False;

         sitemap_product_lists_original = pd.DataFrame();
         if(exists(Props.FilePathProps.sitemapProductListPath) == True):
             sitemap_product_lists_original = pd.read_excel(Props.FilePathProps.sitemapProductListPath, 0, header=0, engine='openpyxl')
             count_row = sitemap_product_lists_original.shape[0]
             if(count_row!=None and count_row>0):
                 isSitemapProductListScraped = True;

         try:
             if(isSitemapProductListScraped):
                 sitemap_product_lists = pd.DataFrame();
                 sitemap_product_lists = sitemap_product_lists_original[sitemap_product_lists_original['isScraped'] == 0]

                 #All Product Urls are Scraped, No Need To Scrape Product Urls!!
                 if(sitemap_product_lists.shape[0]==0):
                     return True;

                 productListItemUrls = await DataServices.Requests.GetProductUrlsAsync(sitemap_product_lists['product_list_url']);

                 product_urls_df = pd.DataFrame()
                 ProductListResults = DataScraper.DataScraper.ScrapeProductListItemUrls(productListItemUrls);

                 if(exists(Props.FilePathProps.productUrlListPath) == True):
                     product_urls_df = pd.read_excel(Props.FilePathProps.productUrlListPath, 0, header=0, engine='openpyxl')
                 else:
                     isFileCreated = FileServices.FileServices.CreateEmptyExcelFile(Props.FilePathProps.productUrlListPath);

                 for itemResult in ProductListResults:
                     sitemap_product_lists_original.loc[sitemap_product_lists_original['product_list_url'] == itemResult.list_url, 'isScraped'] = itemResult.isScraped;
                 
                     if(itemResult.isScraped==0):
                         continue;
                 
                     for productUrl in itemResult.product_urls:
                         excel_title = []
                         excel_value = []
                         
                         excel_title.append("product_list_url")
                         excel_value.append(itemResult.list_url);
                         
                         excel_title.append("product_url")
                         excel_value.append(productUrl);
                         
                         excel_title.append("isScraped")
                         excel_value.append(False);

                         product_urls_df = product_urls_df.append(pd.Series(data=excel_value, index=excel_title), ignore_index=True)

                 #SET IS SCRAPED TYPE TO INTEGER
                 #product_urls_df['isScraped'] = product_urls_df['isScraped'].astype(int)
                 
                 # CREATE EXCEL
                 product_urls_df.to_excel(Props.FilePathProps.productUrlListPath, index=False)
                 sitemap_product_lists_original.to_excel(Props.FilePathProps.sitemapProductListPath, index=False)

                 unscraped_list_count = sitemap_product_lists_original[sitemap_product_lists_original['isScraped'] == 0].shape[0]
                 if(unscraped_list_count==0):
                     isProductUrlsScraped = True;

         except Exception as e:
             LM.LogManager.logMessage("BusinessServices-ScrapeProductUrls-" + str(e), LM.LogType.ERROR);

         return isProductUrlsScraped;

     @staticmethod 
     async def ScrapeProductDetails():

         isProductUrlListScraped = False;
         isProductDetailScraped = False;

         product_url_list_original = pd.DataFrame();
         if(exists(Props.FilePathProps.productUrlListPath) == True):
             product_url_list_original = pd.read_excel(Props.FilePathProps.productUrlListPath, 0, header=0, engine='openpyxl')
             count_row = product_url_list_original.shape[0]
             if(count_row!=None and count_row>0):
                 isProductUrlListScraped = True;

         product_url_list = product_url_list_original[product_url_list_original['isScraped'] == 0]

         try:
             if(isProductUrlListScraped==True):
                 product_url_list = pd.DataFrame();
                 product_url_list = product_url_list_original[product_url_list_original['isScraped'] == 0]

                 #All Product Url List are Scraped, No Need To Scrape Product Details!!
                 if(product_url_list.shape[0]==0):
                     return True;

                 isProductUrlListExists = False;
                 product_detail_df = pd.DataFrame();

                 for slice in DataHelper.DataHelper.slicedata(product_url_list["product_url"], Props.ScrapingWorkProps.scrapingDataSliceSize):
                     productDetails = await DataServices.Requests.GetProductDetailsAsync(slice);

                     records=[]
                     records = DataScraper.DataScraper.ScrapeProductDetails(productDetails);
                     productDetails=[] #cleandata

                     scrapeTimestamp = datetime.today().strftime("%m/%d/%Y, %H:%M:%S")
                     
                     for product in records:
                         productUrl = product.product_url
                         excel_title = []
                         excel_value = []
                     
                         product_url_list_original.loc[product_url_list_original['product_url'] == productUrl, 'isScraped'] = product.isScraped
                     
                         if(product.isScraped==1):
                             excel_title.append("product_url")
                             excel_value.append(productUrl)
                     
                             excel_title.append("product_name")
                             excel_value.append(product.product_name)
                     
                             excel_title.append("product_barcode")
                             excel_value.append(product.product_barcode)
                     
                             excel_title.append("product_stockcode")
                             excel_value.append(product.product_stockcode)
                     
                             excel_title.append("product_unit")
                             excel_value.append(product.product_unit)
                     
                             excel_title.append("product_price")
                             excel_value.append(product.product_price)
                     
                             excel_title.append("product_old_price")
                             excel_value.append(product.product_old_price)
                     
                             i = 1;
                             for cat in product.catList:
                                 excel_title.append("cat" + str(i))
                                 excel_value.append(cat)
                                 i +=1;
                     
                             x = 1;
                             for brand in product.brandList:
                                 excel_title.append("product_brand" + str(x))
                                 excel_value.append(brand)
                                 x +=1;
                     
                             excel_title.append("product_img_url")
                             excel_value.append(Props.APIRoutes.base_url + product.product_img_url)
                     
                             excel_title.append("timestamp")
                             excel_value.append(scrapeTimestamp)
                     
                             newLine = pd.Series(data=excel_value, index=excel_title);
                     
                             product_detail_df = product_detail_df.append(newLine,ignore_index=True)
                 
                 #After 
                 product_url_list_original.to_excel(Props.FilePathProps.productUrlListPath, index=False)
                 
                 #Export DataFrame to Excel
                 product_detail_df.to_excel(Props.FilePathProps.GetProductDataUploadingPath(), index=False)

                 unscraped_product_detail_count = product_url_list_original[product_url_list_original['isScraped'] == 0].shape[0]
                 if(unscraped_product_detail_count==0):
                     isProductDetailScraped = True;

         except Exception as e:
             LM.LogManager.logMessage("BusinessService-ScrapeProductDetails-" + str(e), LM.LogType.ERROR);

         return isProductDetailScraped;