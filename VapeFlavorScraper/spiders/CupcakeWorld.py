import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class CupcakeWorldSpider(scrapy.Spider):
    name = 'CupcakeWorld'
    allowed_domains = ['cupcake-world.co.uk']
    start_urls = ['http://www.cupcake-world.co.uk/index.php?main_page=index&cPath=144_183&sort=20a&page=1']
    num_pages = 1

    def parse(self, response):

        #Get all the flavor items on this page
        item_links = response.css('h3.itemTitle > a::attr(href)').extract()

        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_detail_page)

        self.num_pages = self.num_pages + 1
        if self.num_pages is not 13:
            yield response.follow('http://www.cupcake-world.co.uk/index.php?main_page=index&cPath=144_183&sort=20a&page=' + str(self.num_pages), callback=self.parse)

    def parse_detail_page(self, response):
        name = response.css('#productName::text').extract_first()
        image_url = response.css('#productMainImage')
        image_url = image_url.css('a > img::attr(src)').extract_first()

        if( image_url.find('http') == -1 ):
            image_url = 'http://www.cupcake-world.co.uk/' + image_url

        description = ''

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'Cupcake World'
        item['image_url'] = image_url
        item['description'] = description

        yield item
