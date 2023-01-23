import sys
import time
from datetime import date,datetime
import asyncio
import logging
import warnings
import pandas as pd
from FileServices import FileServices as FS;
from Logger import LogManager as LM
from BusinessServices import BusinessService
from Props import StaticProps as Props


def init_logging(log_file=None, append=False, console_loglevel=logging.INFO):
    """Set up logging to file and console."""
    if log_file is not None:
        if append:
            filemode_val = 'a'
        else:
            filemode_val = 'w'
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s : %(levelname)s :  %(message)s",
                            # datefmt='%m-%d %H:%M',
                            filename=log_file,
                            filemode=filemode_val)
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(console_loglevel)
    # set a format which is simpler for console use
    formatter = logging.Formatter("%(asctime)s : %(message)s")
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    global LOG
    LOG = logging.getLogger(__name__) 

async def main():
    try:
        #Dispose the warnings on console window
        warnings.filterwarnings("ignore")
        init_logging(log_file="logdata.log",append=True, console_loglevel=logging.INFO);
        LM.LogManager.logMessage("PROCESS STARTED - Bilekler MARKET", LM.LogType.INFO);

        startDateTime = datetime.now()
        ###Check Upload Directory
        isDirectoriesAvailable = FS.FileServices.CreateOrCheckAppDirectories();
        if(isDirectoriesAvailable==False):
             LM.LogManager.logMessage("Directories not Avaiable - Process Completed", LM.LogType.INFO);
             return;

        #********************************************************************************************
        #For Single Execution Delete All Files On Process
        FS.FileServices.DeleteOnProcessFiles();
        #********************************************************************************************

        totalTrial = Props.ScrapingWorkProps.scrapingTotalTrialNo;
        trialIndex = 0; 
        for i in range(0,totalTrial):
            try:
                ##get main sitemap
                isProductListsScraped=False;
                if Props.ScrapingWorkProps.scrapeProductListStatus != 0:
                    ##Scrape Main Sitemap Product Lists
                    LM.LogManager.logMessage("TrialNo:" + str(i) + " - Scrape Sitemap Product Lists STARTED : ", LM.LogType.INFO);
                    isProductListsScraped = await BusinessService.BusinessService.ScrapeSitemapProductLists();

                    if(isProductListsScraped==False):
                        LM.LogManager.logMessage("TrialNo:" + str(i) + " - Sitemap Product Lists could not be Scraped.", LM.LogType.ERROR);
                        continue;
                else:
                   isProductListsScraped=True;

                #Scrape Product URLS 
                LM.LogManager.logMessage("TrialNo:" + str(i) + " - ScrapeProductUrls STARTED : ", LM.LogType.INFO)
                isProductUrlsScraped = await BusinessService.BusinessService.ScrapeProductUrls();

                ##Scrape Product Details
                LM.LogManager.logMessage("TrialNo:" + str(i) + " - ScrapeProductDetails STARTED : ", LM.LogType.INFO)
                isProductDetailsScraped = await BusinessService.BusinessService.ScrapeProductDetails();
                
                LM.LogManager.logMessage("TrialNo:" + str(i) + " - Scraped Products File and Location File Moving To Job Directory.. : ", LM.LogType.INFO);
                FS.FileServices.MoveUploadingDirectory();

                endDateTime = datetime.now()
                LM.LogManager.logMessage("TrialNo:" + str(i) + " - StartDateTime: " + startDateTime.strftime("%d/%m/%Y %H:%M:%S") + " - EndDateTime: " + endDateTime.strftime("%d/%m/%Y %H:%M:%S"), LM.LogType.INFO);
                LM.LogManager.logMessage("TrialNo:" + str(i) + " - Process Completed", LM.LogType.INFO);
                LM.LogManager.logMessage("******************************************************", LM.LogType.INFO);

                if(isProductListsScraped==True and isProductUrlsScraped==True and isProductDetailsScraped==True):
                    LM.LogManager.logMessage("TrialNo:" + str(i) + " - All Process Completed Successfully. App will exit!", LM.LogType.INFO);
                    break;
            except Exception as e:
                LM.LogManager.logMessage("TrialNo:" + str(i) + " - Exception -" + str(e), LM.LogType.ERROR);

        #Clean the PROCESS FILES
        LM.LogManager.logMessage("Deletion Process Started for Scraped Sitemap Products, ProductUrl Files" + " sec", LM.LogType.INFO);
        FS.FileServices.DeleteOnProcessFiles();

        #Update isScraped Status to 0 for markets
        if(Props.ScrapingWorkProps.scrapeProductListStatus==0):
            sitemap_product_list_original_df = pd.read_excel(Props.FilePathProps.sitemapProductListPath, 0, header=0, engine='openpyxl')
            for i in range(len(sitemap_product_list_original_df)):
                sitemap_product_list_original_df['isScraped'].values[i] = 0;
            sitemap_product_list_original_df.to_excel(Props.FilePathProps.sitemapProductListPath, index=False)

    except Exception as e:
        LM.LogManager.logMessage("MainApp-" + str(e), LM.LogType.ERROR);

    #*******************Exit From APP***********************************
    sys.exit(0)

#asyncio.run(main())
asyncio.new_event_loop().run_until_complete(main())

