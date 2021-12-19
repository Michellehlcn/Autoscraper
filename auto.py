
import scrapy
from scrapy import Request

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from items import AutoscraperItem
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
#---------Scraping orginal file----------
def generate_start_urls():
    print('Enter the start catalogue number')
    start = input("From: ")
    end = input("To: ")
    return ['https://www.auto-auctions.com.au/catalogue-view.aspx?chid={}'.format(cat_number) for cat_number in range(int(start),int(end))]

class AutoSpider(scrapy.Spider):
    name = 'auto'
    '''allowed_domains = ['auto-auctions.com.au/']
    custom_settings={ 'FEED_URI': "auto_%(time)s.csv",
                       'FEED_FORMAT': 'csv',
                       'DOWNLOAD_DELAY' : 0,
                        'DEPTH_PRIORITY' : 1,
                        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
                        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'}'''
    start_urls = generate_start_urls()

    def parse(self, response):
        item =AutoscraperItem()
        table= response.css('table#gvCatalogue')
        tables =table.xpath('//tbody//a')
        index = len(tables)
        for index,x in enumerate(tables):
            try:
                stock_site=x.css('a').attrib['href'].split('=')[1]
            except IndexError:
                continue
            stock_id = x.css('a').attrib['href'].split('=')[2]
            item['auction'] = index
            item['auction_stock_site']=x.css('a').attrib['href'].split('=')[1]
            item['auction_stock_id']=x.css('a').attrib['href'].split('=')[2]          
            item['auction_stock_title']=x.css('b::text').get()
            item['auction_site'] =response.css('span#label_chcattitle::text').extract()
            item['auction_no'] =response.url.split('=')[1]
            item['auction_pubdate'] =response.css('span#label_chfinish::text').extract()
                #=====Auto Auctions - Sydney========
            if stock_site =='AAV&MTA': 
                absolute_url =('https://auto-auctions.com.au/cp_veh_Inspection_report.aspx?sitekey=AAV&MTA={}'.format(stock_id))
                
                
                request =scrapy.Request(absolute_url,callback=self.parse_aav,errback=self.errback_httpbin,dont_filter=True,cb_kwargs=dict(main_url=response.url))
                request.meta['auction_stock_site'] =item['auction_stock_site']
                request.meta['auction_stock_id'] =item['auction_stock_id']
                request.meta['auction_stock_title']=item['auction_stock_title']
                request.meta['auction_site'] =item['auction_site']
                request.meta['auction_no'] = item['auction_no']
                request.meta['auction_pubdate'] =item['auction_pubdate']
                request.meta['index']=item['auction']
                yield request

                #=======United Auctions NSW Lane1=======
            elif stock_site =='GMA&MTA': 
                absolute_url =('https://www.uaansw.com.au/cp_veh_inspection_report.aspx?sitekey=GMA&MTA={}'.format(stock_id))
                
                
                request =scrapy.Request(absolute_url,callback=self.parse_gma,errback=self.errback_httpbin,dont_filter=True,cb_kwargs=dict(main_url=response.url))
                request.meta['auction_stock_site'] =item['auction_stock_site']
                request.meta['auction_stock_id'] =item['auction_stock_id']
                request.meta['auction_stock_title']=item['auction_stock_title']
                request.meta['auction_site'] =item['auction_site']
                request.meta['auction_no'] = item['auction_no']
                request.meta['auction_pubdate'] =item['auction_pubdate']
                request.meta['index']=item['auction']
                yield request


                #=======CarNet Auctions Western Sydney=======
            elif stock_site =='TMA&MTA': 
                absolute_url =('https://www.carnetauctions.com.au/cp_veh_inspection_report.aspx?sitekey=TMA&MTA={}'.format(stock_id))
                
                
                request =scrapy.Request(absolute_url,callback=self.parse_tma,errback=self.errback_httpbin,dont_filter=True,cb_kwargs=dict(main_url=response.url))
                request.meta['auction_stock_site'] =item['auction_stock_site']
                request.meta['auction_stock_id'] =item['auction_stock_id']
                request.meta['auction_stock_title']=item['auction_stock_title']
                request.meta['auction_site'] =item['auction_site']
                request.meta['auction_no'] = item['auction_no']
                request.meta['auction_pubdate'] =item['auction_pubdate']
                request.meta['index']=item['auction']
                yield request

                    #=======F3 Motor Auctions=======
            elif stock_site =='F3A&MTA': 
                absolute_url =('https://www.f3motorauctions.com.au/cp_veh_inspection_report.aspx?sitekey=F3A&MTA={}'.format(stock_id))
                
                
                request =scrapy.Request(absolute_url,callback=self.parse_f3a,errback=self.errback_httpbin,dont_filter=True,cb_kwargs=dict(main_url=response.url))
                request.meta['auction_stock_site'] =item['auction_stock_site']
                request.meta['auction_stock_id'] =item['auction_stock_id']
                request.meta['auction_stock_title']=item['auction_stock_title']
                request.meta['auction_site'] =item['auction_site']
                request.meta['auction_no'] = item['auction_no']
                request.meta['auction_pubdate'] =item['auction_pubdate']
                request.meta['index']=item['auction']
                yield request

                #=======CarNet Auctions Smithfield=======

            elif stock_site =='CSS&MTA': 
                absolute_url =('https://www.carnetauctions.com.au/cp_veh_inspection_report.aspx?sitekey=CSS&MTA={}'.format(stock_id))
                
                
                request =scrapy.Request(absolute_url,callback=self.parse_css,errback=self.errback_httpbin,dont_filter=True,cb_kwargs=dict(main_url=response.url))
                request.meta['auction_stock_site'] =item['auction_stock_site']
                request.meta['auction_stock_id'] =item['auction_stock_id']
                request.meta['auction_stock_title']=item['auction_stock_title']
                request.meta['auction_site'] =item['auction_site']
                request.meta['auction_no'] = item['auction_no']
                request.meta['auction_pubdate'] =item['auction_pubdate']
                request.meta['index']=item['auction']
                yield request

                #=======CityMotor Auctions=======

            elif stock_site =='CTY&MTA': 
                absolute_url =('https://www.citymotorauction.com.au/cp_veh_inspection_report.aspx?sitekey=CTY&MTA={}'.format(stock_id))
                
                
                request =scrapy.Request(absolute_url,callback=self.parse_cty,errback=self.errback_httpbin,dont_filter=True,cb_kwargs=dict(main_url=response.url))
                request.meta['auction_stock_site'] =item['auction_stock_site']
                request.meta['auction_stock_id'] =item['auction_stock_id']
                request.meta['auction_stock_title']=item['auction_stock_title']
                request.meta['auction_site'] =item['auction_site']
                request.meta['auction_no'] = item['auction_no']
                request.meta['auction_pubdate'] =item['auction_pubdate']
                request.meta['index']=item['auction']
                yield request
                #=======Central Auto Auctions=======

            elif stock_site =='CMA&MTA': 
                absolute_url =('https://www.centralautoauctions.com.au/cp_veh_Inspection_report.aspx?sitekey=CMA&MTA={}'.format(stock_id))
                
                
                request =scrapy.Request(absolute_url,callback=self.parse_cma,errback=self.errback_httpbin,dont_filter=True,cb_kwargs=dict(main_url=response.url))
                request.meta['auction_stock_site'] =item['auction_stock_site']
                request.meta['auction_stock_id'] =item['auction_stock_id']
                request.meta['auction_stock_title']=item['auction_stock_title']
                request.meta['auction_site'] =item['auction_site']
                request.meta['auction_no'] = item['auction_no']
                request.meta['auction_pubdate'] =item['auction_pubdate']
                request.meta['index']=item['auction']
                yield request

                #=======ValleyMotor Auctions=======
            
            elif stock_site =='VMA&MTA': 
                absolute_url =('https://www.valleymotorauctions.com.au/cp_veh_Inspection_report.aspx?sitekey=VMA&MTA={}'.format(stock_id))
                
                
                request =scrapy.Request(absolute_url,callback=self.parse_vma,errback=self.errback_httpbin,dont_filter=True,cb_kwargs=dict(main_url=response.url))
                request.meta['auction_stock_site'] =item['auction_stock_site']
                request.meta['auction_stock_id'] =item['auction_stock_id']
                request.meta['auction_stock_title']=item['auction_stock_title']
                request.meta['auction_site'] =item['auction_site']
                request.meta['auction_no'] = item['auction_no']
                request.meta['auction_pubdate'] =item['auction_pubdate']
                request.meta['index']=item['auction']
                yield request
            #=====Alliance Auctions=============
            elif stock_site =='ALL&MTA': 
                absolute_url =('https://www.allianceauctions.com.au/cp_veh_Inspection_report.aspx?sitekey=ALL&MTA={}'.format(stock_id))
                
                
                request =scrapy.Request(absolute_url,callback=self.parse_alliance,errback=self.errback_httpbin,dont_filter=True,cb_kwargs=dict(main_url=response.url))
                request.meta['auction_stock_site'] =item['auction_stock_site']
                request.meta['auction_stock_id'] =item['auction_stock_id']
                request.meta['auction_stock_title']=item['auction_stock_title']
                request.meta['auction_site'] =item['auction_site']
                request.meta['auction_no'] = item['auction_no']
                request.meta['auction_pubdate'] =item['auction_pubdate']
                request.meta['index']=item['auction']
                yield request      

            else:
                continue


    def parse_aav(self,response,main_url):
        item =AutoscraperItem()

        item['auction'] =response.meta['index']
        item['auction_stock_site']=response.meta['auction_stock_site']
        item['auction_stock_id']=response.meta['auction_stock_id']         
        item['auction_stock_title']=response.meta['auction_stock_title']
        item['auction_site'] =response.meta['auction_site']
        item['auction_no'] =response.meta['auction_no']
        item['auction_pubdate'] =response.meta['auction_pubdate']

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


    def parse_gma(self,response,main_url):
        item =AutoscraperItem()

        item['auction'] =response.meta['index']
        item['auction_stock_site']=response.meta['auction_stock_site']
        item['auction_stock_id']=response.meta['auction_stock_id']         
        item['auction_stock_title']=response.meta['auction_stock_title']
        item['auction_site'] =response.meta['auction_site']
        item['auction_no'] =response.meta['auction_no']
        item['auction_pubdate'] =response.meta['auction_pubdate']

        item['build']=response.css('#lblBuildMMYY::text').extract()
        item['make']=response.css('h2.post-title::text').extract_first().split(' ',2)[1]
        item['name']=response.css('h2.post-title::text').extract_first()
        item['style']=response.css('#lblBody::text').extract()
        item['rego'] =response.css('#lblRego::text').extract()
        item['regExp'] =response.css('#lblRegExpiry::text').extract()
        item['engine'] =response.css('#lblEngineSize::text').extract()
        item['fuel']=response.css('#lblFuelType::text').extract()
        item['trans']=response.css('#lbltransmission::text').extract()
        item['odo']=response.css('#lblKlm::text').extract()
        item['color']=response.css('#lblColour::text').extract()
        item['vin']=response.css('#lblVinNo::text').extract()
        item['link_stock']=response.url
        item['status']=("N/A")
        yield item

    def parse_tma(self,response,main_url):
        item =AutoscraperItem()

        item['auction'] =response.meta['index']
        item['auction_stock_site']=response.meta['auction_stock_site']
        item['auction_stock_id']=response.meta['auction_stock_id']         
        item['auction_stock_title']=response.meta['auction_stock_title']
        item['auction_site'] =response.meta['auction_site']
        item['auction_no'] =response.meta['auction_no']
        item['auction_pubdate'] =response.meta['auction_pubdate']

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
        item['vin']=response.css('#lblVinNo::text').extract()
        item['link_stock']=response.url
        item['status']=("N/A")
        yield item


    def parse_f3a(self,response,main_url):
        item =AutoscraperItem()

        item['auction'] =response.meta['index']
        item['auction_stock_site']=response.meta['auction_stock_site']
        item['auction_stock_id']=response.meta['auction_stock_id']         
        item['auction_stock_title']=response.meta['auction_stock_title']
        item['auction_site'] =response.meta['auction_site']
        item['auction_no'] =response.meta['auction_no']
        item['auction_pubdate'] =response.meta['auction_pubdate']

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
        item['vin']=response.css('#lblVinNo::text').extract()
        item['link_stock']=response.url
        item['status']=("N/A")
        yield item

    def parse_css(self,response,main_url):
        item =AutoscraperItem()

        item['auction'] =response.meta['index']
        item['auction_stock_site']=response.meta['auction_stock_site']
        item['auction_stock_id']=response.meta['auction_stock_id']         
        item['auction_stock_title']=response.meta['auction_stock_title']
        item['auction_site'] =response.meta['auction_site']
        item['auction_no'] =response.meta['auction_no']
        item['auction_pubdate'] =response.meta['auction_pubdate']

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
        item['vin']=response.css('#lblVinNo::text').extract()
        item['link_stock']=response.url
        item['status']=("N/A")
        yield item


    def parse_cty(self,response,main_url):
        item =AutoscraperItem()

        item['auction'] =response.meta['index']
        item['auction_stock_site']=response.meta['auction_stock_site']
        item['auction_stock_id']=response.meta['auction_stock_id']         
        item['auction_stock_title']=response.meta['auction_stock_title']
        item['auction_site'] =response.meta['auction_site']
        item['auction_no'] =response.meta['auction_no']
        item['auction_pubdate'] =response.meta['auction_pubdate']

        item['build']=response.css('#lblBuildMMYY::text').extract()
        item['make']=response.css('#lblMake::text').extract_first()
        item['name']=(response.css('#lblMake::text').extract_first()+(" ")+response.css('#lblModel::text').extract_first()+(" ")+response.css('#lblVariant::text').extract_first()+(" ")+response.css('#lblSeries::text').extract_first())
        item['style']=response.css('#lblBody::text').extract()
        item['rego'] =("N/A")
        item['regExp'] =("N/A")
        item['engine'] =response.css('#lblEngineSize::text').extract()
        item['fuel']=response.css('#lblFuelType::text').extract()
        item['trans']=response.css('#lbltransmission::text').extract()
        item['odo']=response.css('#lblKlm::text').extract()
        item['color']=response.css('#lblColour::text').extract()
        item['vin']=response.css('#lblVinNo::text').extract()
        item['link_stock']=response.url
        item['status']=("N/A")
        yield item


    def parse_cma(self,response,main_url):
        item =AutoscraperItem()

        item['auction'] =response.meta['index']
        item['auction_stock_site']=response.meta['auction_stock_site']
        item['auction_stock_id']=response.meta['auction_stock_id']         
        item['auction_stock_title']=response.meta['auction_stock_title']
        item['auction_site'] =response.meta['auction_site']
        item['auction_no'] =response.meta['auction_no']
        item['auction_pubdate'] =response.meta['auction_pubdate']

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


    def parse_vma(self,response,main_url):
        item =AutoscraperItem()

        item['auction'] =response.meta['index']
        item['auction_stock_site']=response.meta['auction_stock_site']
        item['auction_stock_id']=response.meta['auction_stock_id']         
        item['auction_stock_title']=response.meta['auction_stock_title']
        item['auction_site'] =response.meta['auction_site']
        item['auction_no'] =response.meta['auction_no']
        item['auction_pubdate'] =response.meta['auction_pubdate']

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
        item['odo']=response.css('#lblKlm::text').extract()
        item['color']=response.css('#lblColour::text').extract()
        item['vin']=response.css('#lblVinNo::text').extract()
        item['link_stock']=response.url
        try:
            item['status']=response.css('div.price::text').extract().strip(' ')
        except AttributeError:
            item['status']=("N/A")
            pass
        yield item

    def parse_alliance(self,response,main_url):
        item =AutoscraperItem()

        item['auction'] =response.meta['index']
        item['auction_stock_site']=response.meta['auction_stock_site']
        item['auction_stock_id']=response.meta['auction_stock_id']         
        item['auction_stock_title']=response.meta['auction_stock_title']
        item['auction_site']=response.meta['auction_site']
        item['auction_no']=response.meta['auction_no']
        item['auction_pubdate'] =response.meta['auction_pubdate']


        item['link_stock']=response.url
        if response.css('#lblMake::text').extract() =='Label':
            item['status']=("SOLD")
            item['build']=("N/A")
            item['make']=("N/A")
            item['name']=("N/A")
            item['style']=("N/A")
            item['rego']=("N/A")
            item['regExp']=("N/A")
            item['engine']=("N/A")
            item['fuel']=("N/A")
            item['trans']=("N/A")
            item['odo']=("N/A")
            item['color']=("N/A")
            item['vin']=("N/A")
        else:
            item['status']=("N/A")
            item['build']=response.css('#lblBuildMMYY::text').extract()
            item['make']=response.css('#lblMake::text').extract_first()
            item['name']=(response.css('#lblMake::text').extract_first()+(" ")+response.css('#lblModel::text').extract_first()+(" ")+response.css('#lblVariant::text').extract_first()+(" ")+response.css('#lblSeries::text').extract_first())
            item['style']=response.css('#lblBody::text').extract()
            item['rego'] =response.css('#lblBody::text').extract()
            item['regExp']=response.css('#lblRegExpiry::text').extract()
            item['engine']=response.css('#lblEngineSize::text').extract()
            item['fuel']=response.css('#lblFuelType::text').extract()
            item['trans']=response.css('#lblTransmission::text').extract()
            item['odo']=response.css('#lblKlm::text').extract()
            item['color']=response.css('#lblColour::text').extract()
            item['vin']=response.css('#lblVinNo::text').extract()
        yield item

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

#-------------------------------


'''process = CrawlerProcess(settings = {
        'FEED_URI': 'auto.csv',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY' : 0,
        'DEPTH_PRIORITY' : 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'
    })

process.crawl(AutoSpider)
process.start()'''


