import scrapy


class BrightspiderSpider(scrapy.Spider):
    name = 'brightspider'
    allowed_domains = ['brighton.co.id']
    start_urls = ['http://brighton.co.id/']

    def parse(self, response):
        pass
