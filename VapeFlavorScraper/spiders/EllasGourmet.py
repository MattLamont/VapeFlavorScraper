import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class EllasGourmetSpider(scrapy.Spider):
    name = 'EllasGourmet'
    allowed_domains = ['highdesertvapes.com']
    start_urls = ['https://highdesertvapes.com/categories/DIY/DIY-Flavors/Ella%27s-Gourmet-Flavor-Drops/']

    def parse(self, response):

        #Get all the flavor items on this page
        item_links = response.css('div.ProductDetails > strong > a::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_detail_page)

        #Get the next page of items
        next_page = response.css('div.CategoryPagination > div.FloatRight > a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail_page(self, response):
        name = response.css('#ProductDetails > div > h2::text').extract_first()
        image_url = response.css('#ProductDetails > div > div.ProductThumb > div.ProductThumbImage > a > img::attr(src)').extract_first()

        description = ''

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'Ella\'s Gourmet'
        item['image_url'] = image_url
        item['description'] = description

        yield item
