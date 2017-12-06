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
        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_detail_page)

        #Get the next page of items
        #next_page = response.css('div.no-pad-lr > div.center > ul.pagination > li > a::attr(href)').extract_first()
        next_page = 'https://www.nicvape.com/e-flavors?pi=' + self.page_number
        page_number = page_number + 1
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail_page(self, response):
        name = response.css('h1.ProductDetailsProductName > span::text').extract()[0]
        image_url = response.css('div.thumbnail > a.main-product-photo > img::attr(src)').extract()

        #if len(image_url) is 0:
        #    image_url = response.css('div.ty-product-img > a > img::attr(src)').extract()

        description = response.css('span.ProductDetailsBullets > ul > li').extract()

        #if len(description) is 0:
        #    description = response.css('div.wysiwyg-content > div::text').extract()[0]

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'NicVape'
        item['image_url'] = image_url
        item['description'] = description

        yield item
