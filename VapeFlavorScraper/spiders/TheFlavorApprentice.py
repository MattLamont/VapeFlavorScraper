import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class TheFlavorApprenticeSpider(scrapy.Spider):
    name = 'TheFlavorApprentice'
    allowed_domains = ['shop.perfumersapprentice.com']
    start_urls = [
        'https://shop.perfumersapprentice.com/c-231-cereal-flavors.aspx',
        'https://shop.perfumersapprentice.com/c-154-chocolate-vanilla-flavors.aspx',
        'https://shop.perfumersapprentice.com/c-149-coffee-flavors.aspx',
        'https://shop.perfumersapprentice.com/c-155-fruit-and-vegetable-flavors.aspx',
        'https://shop.perfumersapprentice.com/c-155-fruit-and-vegetable-flavors.aspx',
        'https://shop.perfumersapprentice.com/c-151-menthol-and-mint.aspx',
        'https://shop.perfumersapprentice.com/c-157-nutty-flavors.aspx',
        'https://shop.perfumersapprentice.com/c-156-savory-flavors.aspx',
        'https://shop.perfumersapprentice.com/c-152-spices-and-floral.aspx',
        'https://shop.perfumersapprentice.com/c-150-sweet-or-sour-flavors.aspx',
        'https://shop.perfumersapprentice.com/c-158-tea-soda-and-liqueur-flavors.aspx',
        'https://shop.perfumersapprentice.com/c-153-tobacco-and-wood-flavors.aspx',
    ]

    def parse(self, response):

        #Get all the flavor items on this page
        item_links = response.css('#ctl00_PageContent_pnlContent > ul > li > a::attr(href)').extract()

        #If there are no flavor items on this page, then get out
        if len(item_links) is 0:
            return

        #Process each flavor item
        for a in item_links:
            yield scrapy.Request( 'https://shop.perfumersapprentice.com' + a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        name = response.css('#ctl00_PageContent_pnlContent > h2::text').extract()[0]

        image_url = response.css('div.medium-image-wrap > img::attr(src)').extract()
        if len( image_url ) is not 0:
            image_url = 'https://shop.perfumersapprentice.com' + image_url[0]

        else:
            image_url = ''

        description = ''

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'The Flavor Apprentice'
        item['image_url'] = image_url
        item['description'] = description

        yield item
