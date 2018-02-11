import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class AtmosLabSpider(scrapy.Spider):
    name = 'AtmosLab'
    allowed_domains = ['atmoslab.com']
    start_urls = [
        'http://atmoslab.com/catalog/diy/liquidware/flavours/tobacco-flavours',
        'http://atmoslab.com/catalog/diy/liquidware/flavours/fruit-flavours',
        'http://atmoslab.com/catalog/diy/liquidware/flavours/sweet-and-drinks-flavours',
        'http://atmoslab.com/catalog/diy/liquidware/flavours/herbs-and-spices-flavours'
    ]

    def parse(self, response):

        #Get all the flavor items on this page
        item_links = response.css('tbody > tr > td:nth-child(2) > a::attr(href)').extract()

        #If there are no flavor items on this page, then get out
        if len(item_links) is 0:
            return

        #Process each flavor item
        for a in item_links:
            yield scrapy.Request( 'http://atmoslab.com' + a, callback=self.parse_detail_page)

        next_page = response.css('li.pager-next > a::attr(href)').extract()
        if len(next_page) is not 0:
            yield response.follow( 'http://atmoslab.com' + next_page[0], callback=self.parse)

    def parse_detail_page(self, response):
        name = response.css('#cont-col > div > h2::text').extract()[0]
        image_url = response.css('div.product-image > div.main-product-image > a > img::attr(src)').extract()

        description = response.css('div.product-body > p:nth-child(1)::text').extract()

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'Atmos Lab'
        item['image_url'] = image_url
        item['description'] = description

        yield item
