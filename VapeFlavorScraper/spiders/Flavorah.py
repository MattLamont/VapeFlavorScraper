import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class FlavorahSpider(scrapy.Spider):
    name = 'Flavorah'
    allowed_domains = ['store.flavorah.com']
    start_urls = [
        'http://store.flavorah.com/All-Vaping-Flavors_c_8.html',
    ]

    def parse(self, response):

        item_links = response.css('div.product-item > div.name > a::attr(href)').extract()

        for link in item_links:
            yield scrapy.Request( 'http://store.flavorah.com/' + link , callback=self.parse_detail_page)

        #Get the next page of items
        next_page = response.css('a.category-viewall::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

    def parse_detail_page(self, response):

        name = response.css('div.secondary > h1.page_headers::text').extract_first()
        image_url = response.css('#listing_main_image_link > img::attr(src)').extract_first()
        image_url = 'http://store.flavorah.com/' + image_url

        description = response.css('#tab-1 > div::text').extract_first()

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'Flavorah'
        item['image_url'] = image_url
        item['description'] = description

        yield item
