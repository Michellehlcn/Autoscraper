import pandas as pd

from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from twisted.internet import defer, reactor
from multiprocessing import Process, Queue
from auto_aav import AavSpider 
#-----Running multi-spiders------------


process_aav = CrawlerProcess(settings = {
        'FEED_URI': 'aav.csv',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY' : 0,
        'DEPTH_PRIORITY' : 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'
    })
process_all = CrawlerProcess(settings = {
        'FEED_URI': 'all.csv',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY' : 0,
        'DEPTH_PRIORITY' : 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'
    })
process_caa = CrawlerProcess(settings = {
        'FEED_URI': 'caa.csv',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY' : 0,
        'DEPTH_PRIORITY' : 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'
    })

process_cma = CrawlerProcess(settings = {
        'FEED_URI': 'cma.csv',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY' : 0,
        'DEPTH_PRIORITY' : 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'
    })

process_css = CrawlerProcess(settings = {
        'FEED_URI': 'css.csv',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY' : 0,
        'DEPTH_PRIORITY' : 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'
    })

process_cty = CrawlerProcess(settings = {
        'FEED_URI': 'cty.csv',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY' : 0,
        'DEPTH_PRIORITY' : 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'
    })

process_f3a = CrawlerProcess(settings = {
        'FEED_URI': 'f3a.csv',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY' : 0,
        'DEPTH_PRIORITY' : 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'
    })
process_vma = CrawlerProcess(settings = {
        'FEED_URI': 'vma.csv',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY' : 0,
        'DEPTH_PRIORITY' : 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'
    })

process_gma = CrawlerProcess(settings = {
        'FEED_URI': 'gma.csv',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY' : 0,
        'DEPTH_PRIORITY' : 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'
    })
process_tma = CrawlerProcess(settings = {
        'FEED_URI': 'tma.csv',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY' : 0,
        'DEPTH_PRIORITY' : 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'
    })


@defer.inlineCallbacks
def crawl():    
        yield process_aav.crawl(AavSpider)

        from auto_all import AllSpider
        yield process_all.crawl(AllSpider)

        from auto_caa import CaaSpider        
        yield process_caa.crawl(CaaSpider)

        from auto_cma import CmaSpider
        yield process_cma.crawl(CmaSpider)

        from auto_css import CssSpider
        yield process_css.crawl(CssSpider)

        from auto_cty import CtySpider
        yield process_cty.crawl(CtySpider)

        from auto_f3a import F3aSpider
        yield process_f3a.crawl(F3aSpider)

        from auto_vma import VmaSpider
        yield process_vma.crawl(VmaSpider)

        from auto_gma import GmaSpider
        yield process_gma.crawl(GmaSpider)

        from auto_tma import TmaSpider
        yield process_tma.crawl(TmaSpider)
        reactor.stop()

crawl()
reactor.run()
