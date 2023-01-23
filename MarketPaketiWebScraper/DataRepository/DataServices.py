import asyncio
from DataRepository import BaseRepository
from Props import StaticProps as Props
from Logger import LogManager as LM


class Requests(object):

     @staticmethod
     async def GetSitemapProductListsAsync():
         try:
             getResult = await BaseRepository.main([Props.APIRoutes.base_sitemap]);
             return getResult;

         except Exception as e:
             LM.LogManager.logMessage("DataServices-GetProductListUrls-" + str(e), LM.LogType.ERROR);
             
         return [];

     @staticmethod
     async def GetProductUrlsAsync(productPageList):
         try:
             result = await BaseRepository.main(productPageList);
             return result;
         except Exception as e:
             LM.LogManager.logMessage("DataServices-GetProductUrls-" + str(e), LM.LogType.ERROR);
             
         return [];

     @staticmethod
     async def GetProductDetailsAsync(productUrls):

         try:
             marketCategories = await BaseRepository.main(productUrls);
             return marketCategories;
         except Exception as e:
             LM.LogManager.logMessage("DataServices-GetProductDetailsAsync-" + str(e), LM.LogType.ERROR);
             
         return [];


     