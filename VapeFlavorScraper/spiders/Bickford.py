import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem
from selenium import webdriver
import time


class BickfordSpider(scrapy.Spider):
    name = 'Bickford'
    allowed_domains = ['bickfordflavors.com']
    start_urls = [
        'https://www.bickfordflavors.com/collections/water-soluble-flavors/water-soluble-flavor'
    ]

    def parse(self, response):

        driver = webdriver.Chrome("./drivers/chromedriver.exe")
        driver.get(response.url)

        for i in [0,4]:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)


        item_links = driver.find_elements_by_css_selector('div.product > p > a')

        for link in item_links:
            logging.info( link.get_attribute('href'))
            yield scrapy.Request( link.get_attribute('href'), callback=self.parse_detail_page)

        driver.close()

    def parse_detail_page(self, response):

        name = response.css('#detail > h1::text').extract_first()
        image_url = response.css('div.singleimage > a > img::attr(src)').extract_first()

        description = response.css('div.description.contentsection > div > p:nth-child(1)::text').extract()

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'Bickford'
        item['image_url'] = image_url
        item['description'] = description

        yield item
