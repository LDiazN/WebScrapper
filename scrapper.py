"""
    Main functions you can call in other places
"""
from scrapy.crawler import CrawlerProcess
from scrapy         import signals
from settings import URL_TO_SPIDERS, CRAWLER_SETTINGS

_process = CrawlerProcess(CRAWLER_SETTINGS)

def scrape(url : str):
    """
        Main scrapper function 
    """
    # Items accumulator
    items = []
    
    # callback function to collect items on the fly
    def items_scrapped(item, response, spider): 
        items.append(item)

    # Get corresponding spider from url
    spider = _get_spider_from_url(url)
    spider.start_urls = [url]

    # create crawler for this spider, connect signal so we can collect items
    crawler = _process.create_crawler(spider)
    crawler.signals.connect(items_scrapped, signal=signals.item_scraped)

    # start scrapping
    _process.crawl(crawler)
    _process.start()

    # return post processed scrapped objects
    return items

def _get_spider_from_url(url : str):
    """
        Validates if this url is scrapable and returns its 
        corresponding spider when it is
    """

    for known_url in URL_TO_SPIDERS.keys():
        if known_url in url:
            return URL_TO_SPIDERS[known_url]

    raise ValueError(f"Unable to scrap this site: {url}")
