import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class BakerFlavorsSpider(scrapy.Spider):
    name = 'BakerFlavors'
    allowed_domains = ['http://baker-flavors.blogspot.ru']
    start_urls = ['http://baker-flavors.blogspot.ru/2013/10/we-accept-orders-on-our-email.html']
    page_number = 2

    def parse(self, response):

        #Process each flavor item
        for item in self.parse_detail_page( response ):
            yield item

    def parse_detail_page(self, response ):

        for index in (2,96):
            #nameSelector = '#Blog1 > div.blog-posts.hfeed > div.post.hentry > div.post-body.entry-content > table > tbody > tr:nth-child({}) > td:nth-child(2) > a > b::text'.format(index)
            nameSelector = 'table > tbody > tr:nth-child({}) > td:nth-child(2) > a > b'.format(index)
            logging.info( nameSelector)
            name = response.css(nameSelector).extract()
            logging.info( name)
            #image_url = response.css('img.productView-image--default::attr(src)').extract()[0]
            image_url = ''
            description = ''

            item = VapeFlavorItem()
            item['name'] = name
            item['link'] = 'http://baker-flavors.blogspot.ru/2013/10/we-accept-orders-on-our-email.html'
            item['manufacturer'] = 'Mt Baker Vapor'
            item['image_url'] = image_url
            item['description'] = description

            yield item
