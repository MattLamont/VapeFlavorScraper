import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class NicvapeSpider(scrapy.Spider):
    name = 'NicVape'
    allowed_domains = ['nicvape.com']
    start_urls = ['https://www.nicvape.com/e-flavors']
    page_number = 2

    def parse(self, response):

        #Get all the flavor items on this page
        item_links = response.css('div.caption > div.no-m-b > a::attr(href)').extract()

        #If there are no flavor items on this page, then get out
        if len(item_links) is 0:
            return

        #Process each flavor item
        for a in item_links:
            yield scrapy.Request( 'https://www.nicvape.com' + a, callback=self.parse_detail_page)

        #Get the next page of items
        next_page = 'https://www.nicvape.com/e-flavors?pi=' + str(self.page_number)
        self.page_number = self.page_number + 1
        yield response.follow(next_page, callback=self.parse)

    def parse_detail_page(self, response):
        name = response.css('h1.ProductDetailsProductName > span::text').extract()[0]
        image_url = 'https://www.nicvape.com/e-flavors' + response.css('div.thumbnail > a.main-product-photo > img::attr(src)').extract()[0]

        description = response.css('span.ProductDetailsBullets > ul > li').extract()
        description = ''.join( description )

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'NicVape'
        item['image_url'] = image_url
        item['description'] = description

        yield item
