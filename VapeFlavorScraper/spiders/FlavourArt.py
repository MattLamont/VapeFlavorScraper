import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class FlavourartSpider(scrapy.Spider):
    name = 'FlavourArt'
    allowed_domains = ['flavourart.com']
    start_urls = ['https://flavourart.com/en/store/flavors/']

    def parse(self, response):

        #Get all the flavor items on this page
        item_links = response.css('.cm-ajax > .ty-grid-list__image > a::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_detail_page)

        #Get the next page of items
        next_page = response.css('a.ty-pagination__next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail_page(self, response):
        name = response.css('h1.ty-product-block-title::text').extract()[0]
        image_url = response.css('div.ty-product-img > a::attr(href)').extract()

        if len(image_url) is 0:
            image_url = response.css('div.ty-product-img > a > img::attr(src)').extract()

        description = response.css('div.wysiwyg-content > div > p::text').extract()

        if len(description) is 0:
            description = response.css('div.wysiwyg-content > div::text').extract()[0]

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'Flavour Art'
        item['image_url'] = image_url
        item['description'] = description

        yield item
