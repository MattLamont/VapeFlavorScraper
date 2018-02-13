import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class SilverCloudEstatesSpider(scrapy.Spider):
    name = 'SilverCloudEstates'
    allowed_domains = ['apexflavors.com']
    start_urls = [
        'https://www.apexflavors.com',
    ]

    def parse(self, response):

        item_links = response.css('div > div > div > ul > li:nth-child(1) > a::text').extract()

        for link in item_links:
            name = link
            image_url = 'https://www.apexflavors.com/images/Apex%20Flavors_tagline-180.png'

            description = ''

            item = VapeFlavorItem()
            item['name'] = name
            item['link'] = response.url
            item['manufacturer'] = 'Silver Cloud Estates'
            item['image_url'] = image_url
            item['description'] = description

            yield item



    def parse_detail_page(self, response):

        name = response.css('#primary_block > h1::text').extract_first()
        image_url = response.css('#bigpic::attr(src)').extract_first()

        description = ''

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'SilverCloudEstates'
        item['image_url'] = image_url
        item['description'] = description

        yield item
