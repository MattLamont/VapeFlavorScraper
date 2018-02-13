import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem
from selenium import webdriver
import time


class MolinberrySpider(scrapy.Spider):
    name = 'Molinberry'
    allowed_domains = ['diyvaporsupply.com']
    start_urls = [
        'https://www.diyvaporsupply.com/brands/Molin-Berry.html?sort=alphaasc'
    ]

    def parse(self, response):

        driver = webdriver.Chrome("./drivers/chromedriver.exe")
        driver.get(response.url)

        for i in range(0,6):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)


        item_links = driver.find_elements_by_css_selector('h4.card-title > a')
        logging.info( len(item_links))

        for link in item_links:
            yield scrapy.Request( link.get_attribute('href'), callback=self.parse_detail_page)

        driver.close()

    def parse_detail_page(self, response):

        name = response.css('h1.productView-title::text').extract_first()
        image_url = response.css('figure.productView-image::attr(data-zoom-image)').extract_first()

        description = ''

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'Molinberry'
        item['image_url'] = image_url
        item['description'] = description

        yield item
