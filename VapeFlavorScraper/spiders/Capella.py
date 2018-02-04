import scrapy
import logging
import re
from VapeFlavorScraper.items import VapeFlavorItem


class CapellaSpider(scrapy.Spider):
    name = 'Capella'
    allowed_domains = ['capellaflavors.com']
    start_urls = ['https://www.capellaflavors.com/13ml?p=1','https://www.capellaflavors.com/13ml?p=2']

    def parse(self, response):

        #Get all the flavor items on this page
        item_links = response.css('#maincontent > div.columns > div.column.main > div.products.wrapper.toolbar-container.grid.products-grid > ol > li > div.product-item-info > a::attr(href)').extract()

        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        name = response.css('#maincontent > div.columns > div > div.product-info-main > div > div.left > div.main-info-wrapper > div.page-title-wrapper > h1::text').extract()[0]
        name = re.sub(r'[\r][\n][\t]' , '' , name ).strip()
        name = re.sub(r'13ml' , '' , name ).strip()
        image_url = response.css('div.fotorama__stage > img::attr(src)').extract()[0]

        description = name

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'Capella'
        item['image_url'] = image_url
        item['description'] = description

        yield item
