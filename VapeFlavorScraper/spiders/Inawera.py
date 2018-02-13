import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class InaweraSpider(scrapy.Spider):
    name = 'Inawera'
    allowed_domains = ['inaweraflavours.com']
    start_urls = [
        'http://www.inaweraflavours.com/en/7-e-flavours?n=50&id_category=7',
    ]

    def parse(self, response):

        item_links = response.css('#product_list > li > div > h3 > a::attr(href)').extract()

        for link in item_links:
            yield scrapy.Request( link , callback=self.parse_detail_page)

        #Get the next page of items
        next_page = response.css('#pagination_next > a::attr(href)').extract_first()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail_page(self, response):

        name = response.css('#primary_block > h1::text').extract_first()
        image_url = response.css('#bigpic::attr(src)').extract_first()

        description = ''

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'Inawera'
        item['image_url'] = image_url
        item['description'] = description

        yield item
