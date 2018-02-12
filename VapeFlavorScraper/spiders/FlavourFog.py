import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class FlavourFogSpider(scrapy.Spider):
    name = 'FlavourFog'
    allowed_domains = ['flavourfog.com']
    start_urls = ['https://www.flavourfog.com/category_s/1907.htm']

    def parse(self, response):

        #Get all the flavor items on this page
        item_links = response.css('a.productnamecolor::attr(href)').extract()
        logging.info( item_links[0])
        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        name = response.css('font.productnamecolorLARGE > span::text').extract_first()
        image_url = response.css('#product_photo::attr(src)').extract_first()

        description = ''

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'Flavour Fog'
        item['image_url'] = image_url
        item['description'] = description

        yield item
