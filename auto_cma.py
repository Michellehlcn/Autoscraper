
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
    end = int(df_start.iloc[8])
    no = 1000
    start = end - no
    print(start)
    return ['https://www.centralautoauctions.com.au/cp_veh_Inspection_report.aspx?sitekey=CMA&MTA={}'.format(cat_number) for cat_number in range(int(start),int(end))]

class CmaSpider(scrapy.Spider):
    name = 'auto'
    '''allowed_domains = ['auto-auctions.com.au/']
    custom_settings={ 'FEED_URI': "auto_aav%(time)s.csv",
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
        item['make']=response.css('#lblMake::text').extract_first()
        item['name']=response.css('h2.post-title::text').extract_first()
        item['style']=response.css('#lblBody::text').extract()
        item['rego'] =response.css('#lblRego::text').extract()
        item['regExp'] =response.css('#lblRegExpiry::text').extract()
        item['engine'] =response.css('#lblEngineSize::text').extract()
        item['fuel']=response.css('#lblFuelType::text').extract()
        item['trans']=response.css('#lblTransmission::text').extract()
        item['odo']=response.css('#lblKlm::text').extract()
        item['color']=response.css('#lblColour::text').extract()
        item['vin']=("N/A")
        item['link_stock']=response.url
        item['status']=("N/A")
        yield item

'''process = CrawlerProcess(settings = {
        'FEED_URI': 'auto_cma.csv',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY' : 0,
        'DEPTH_PRIORITY' : 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'
    })

process.crawl(CmaSpider)
process.start()'''
