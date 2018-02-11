import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem
from selenium import webdriver
import time
import re


class LorAnnSpider(scrapy.Spider):
    name = 'LorAnn'
    allowed_domains = ['lorannoils.com']
    start_urls = [
        'http://www.lorannoils.com/1-dram-size'
    ]

    def __init__(self):
        self.driver = webdriver.Chrome("./drivers/chromedriver.exe")

    def __del__(self):
        self.driver.close()

    def parse(self, response):

        self.driver.get(response.url)

        while True:
            next = self.driver.find_element_by_css_selector('#cmdViewMore')

            try:
                next.click()
                time.sleep(3)
            except:
                break

        item_links = self.driver.find_elements_by_css_selector('li.product-title > a')

        for item in item_links:
            yield scrapy.Request( item.get_attribute('href'), callback=self.parse_detail_page)

    def parse_detail_page(self, response):

        name = response.css('div.span8 > div.row-fluid.no-margin > h1::text').extract()[0]
        logging.info( name )
        name = re.sub(r'Flavor' , '' , name ).strip()
        name = re.sub(r'1 dram' , '' , name ).strip()
        logging.info( name )
        image_url = response.css('#product-detail-gallery-main-img::attr(src)').extract()[0]
        image_url = 'http://www.lorannoils.com' + image_url

        description = response.css('div.product-details-desc::text').extract()

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'LorAnn'
        item['image_url'] = image_url
        item['description'] = description

        yield item
