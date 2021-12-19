# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


import json    
from collections import OrderedDict

class OrderedItem(scrapy.Item):
    def __init__(self, *args, **kwargs):
        self._values = OrderedDict()
        if args or kwargs:
            for k, v in six.iteritems(dict(*args, **kwargs)):
                self[k] = v

    def __repr__(self):
        return json.dumps(OrderedDict(self),ensure_ascii = False)  
        #ensure_ascii = False ,it make characters show in cjk appearance.

class AutoscraperItem(OrderedItem):
    # define the fields for your item here like:
    # name = scrapy.Field()

    auction=scrapy.Field()
    auction_stock_site=scrapy.Field()
    auction_stock_id=scrapy.Field()      
    auction_stock_title=scrapy.Field()
    auction_site=scrapy.Field()
    auction_no=scrapy.Field()
    auction_pubdate=scrapy.Field()
    make =scrapy.Field()
    name =scrapy.Field()
    style =scrapy.Field()
    build =scrapy.Field()  
    rego =scrapy.Field()
    regExp =scrapy.Field()
    engine =scrapy.Field()
    fuel =scrapy.Field()
    trans =scrapy.Field()
    odo =scrapy.Field()
    color =scrapy.Field()
    vin =scrapy.Field()   
    status =scrapy.Field()
    link_stock =scrapy.Field()
    pass


