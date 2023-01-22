import asyncio
import aiohttp
import time
import json
from Models import HtmlResponse as HResponse
from Logger import LogManager as LM
from Props import StaticProps as Props


async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))

async def get_async(url, session, results):
    try:
        async with session.get(url) as response:
            resultData = HResponse.HtmlResponse()
            resultData.item_url = url
            statusCode = response.status
            r = await response.text()
            resultData.status_code = statusCode;
            resultData.html_detail = r;
            #if(statusCode==200):
            #     resultData.html_detail = r;
            #else:
            #    LM.LogManager.logMessage("API Response Error: " + url + " : StatusCode:" + str(statusCode) + " : " + str(r) , LM.LogType.EXCEPTION);
            #    resultData.html_detail = ""
            results.append(resultData)
    #except aiohttp.ClientConnectorError as e:
    #      print('Connection Error', str(e))
    except (Exception, aiohttp.ClientConnectorError) as error:
        LM.LogManager.logMessage("URL = " + url + " - Error = " +  str(error), LM.LogType.EXCEPTION);

async def main(urls):
    headers={'Accept-Language' : 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Content-Type': 'text/html; charset=utf-8'}

    results = []
    #headers = {"User-Agent": "Mozilla/5.0"}
    conn = aiohttp.TCPConnector(limit=None, ttl_dns_cache=None)
    session = aiohttp.ClientSession(connector=conn,trust_env=True)
    conc_req = Props.ScrapingWorkProps.parallelWebRequestConcReqSize;

    try:
        totalUrlNo = str(len(urls));
        LM.LogManager.logMessage("BASE_Repository => TotalURL = " + totalUrlNo + " - Web Requests Started", LM.LogType.INFO);

        await gather_with_concurrency(conc_req, *[get_async(i, session, results) for i in urls])

        LM.LogManager.logMessage("BASE_Repository => TotalURL = " + totalUrlNo + " - Web Requests Ended", LM.LogType.INFO);

    except (Exception, aiohttp.ClientError, asyncio.TimeoutError) as error:
        LM.LogManager.logMessage("Base_repository-Main-Error" + str(error), LM.LogType.ERROR);
    finally:
        await session.close()
        return results








