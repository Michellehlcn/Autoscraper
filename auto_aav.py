
import scrapy
from scrapy import Request

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.crawler import CrawlerProcess
from items import AutoscraperItem

from datetime import date
import pandas as pd

def generate_start_urls():
    df_start = pd.read_csv('start.csv')
    end = int(df_start.iloc[6])
    no = 1000
    start = end - no
    print(start)
    return ['https://auto-auctions.com.au/cp_veh_Inspection_report.aspx?sitekey=AAV&MTA={}'.format(cat_number) for cat_number in range(int(start),int(end))]

class AavSpider(scrapy.Spider):
    name = 'auto'
    allowed_domains = ['auto-auctions.com.au/']
    '''custom_settings={ 'FEED_URI': "auto_aav.csv",
                       'FEED_FORMAT': 'csv',
                       'DOWNLOAD_DELAY' : 0,
                        'DEPTH_PRIORITY' : 1,
                        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
                        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'}'''

    start_urls = generate_start_urls()

    def parse(self, response):
        item =AutoscraperItem()
        item['auction_pubdate'] = str(date.today())
        item['build']=response.css('#lblBuildMMYY::text').extract()
        heading =response.css('div.heading')
        item['make']=heading.css('div.title::text').extract_first().split(' ',2)[1]
        item['name']=heading.css('div.title::text').extract_first()
        item['style']=response.css('#lblBody::text').extract()
        item['rego'] =response.css('#lblRego::text').extract()
        item['regExp'] =response.css('#lblRegExpiry::text').extract()
        item['engine'] =response.css('#lblEngineSize::text').extract()
        item['fuel']=response.css('#lblFuelType::text').extract()
        item['trans']=response.css('#lblTransmission::text').extract()
        item['odo']=response.css('#lblOdometer::text').extract()
        item['color']=response.css('#lblColour::text').extract()
        item['vin']=response.css('#lblVinNo::text').extract()
        item['link_stock']=response.url
        item['status']=("N/A")
        yield item

'''process = CrawlerProcess(settings = {
        'FEED_URI': 'aav.csv',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY' : 0,
        'DEPTH_PRIORITY' : 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'
    })

process.crawl(AavSpider)
process.start()'''
