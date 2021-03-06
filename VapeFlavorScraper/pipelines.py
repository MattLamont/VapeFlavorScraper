# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import requests
import logging
import json
import time

from scrapy.utils.project import get_project_settings


class VapeflavorscraperPipeline(object):
    def process_item(self, item, spider):
        return item

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['name'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['name'])
            return item

class EmptyDescriptionPipeline(object):

    def process_item(self, item, spider):
        if len(item['description']) is 0:
            item['description'] = item['name']

        return item

class AddToDatabasePipeline(object):

    url = ''
    username = ''
    password = ''
    token = ''
    disabled = True

    def __init__(self, username , password , url ):
        self.username = username
        self.password = password
        self.url = url

        if url is None:
            self.disabled = True
            return

        self.disabled = False
        auth_url = str(self.url) + "/auth/login"
        payload = {'email': self.username , 'password': self.password }

        r = requests.post( auth_url , data=payload )
        self.token = 'Bearer ' + r.json()['token']

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings['USERNAME'] , settings['PASSWORD'] , settings['URL'] )

    def process_item(self, item, spider):

        #if this is not production mode: skip writing to database
        if self.disabled is True:
            item['isNewFlavor'] = True
            return item

        #setup the JSON payload
        payload = {'name': item['name'], 'description': item['description'], 'image_url': item['image_url'] , 'manufacturer': item['manufacturer'], 'link': item['link']}

        #setup up the request headers for Authorization
        headers = {'Authorization' : self.token}

        #setup the flavor get URL where we will check if this flavor already exists
        flavorGetURL = self.url + '/flavor?where={"name":"'+ item['name']  +'"}'

        #check for the current flavor already in the database
        res = requests.get( flavorGetURL , headers=headers )

        #if the flavor is already in the database, then we will just do an update with any new data
        if len( res.json() ) is not 0:
            flavorId = res.json()[0]['id']
            flavorPutURL = self.url + '/flavor/' + str(flavorId)
            item['isNewFlavor'] = False
            res = requests.put( flavorPutURL , headers=headers , data=payload )
            logging.info( "Updated Item: " + item['name'] )

        #otherwise we will create a new flavor in the database
        else:
            flavorPutURL = self.url + '/flavor'
            res = requests.post( flavorPutURL , headers=headers , data=payload )
            logging.info( res.status_code )
            item['isNewFlavor'] = True
            logging.info( "Created Item: " + item['name'] )

        return item

class JsonWriterPipeline(object):

    def open_spider(self, spider):

        timeString = time.strftime( "%Y-%m-%dT%H-%M-%S" , time.localtime() )
        updatedFileName = "data/%s/Updated_%s.json" % (spider.name , timeString )
        createdFileName = "data/%s/Created_%s.json" % (spider.name , timeString )
        self.updatedFlavorFile = open(updatedFileName, 'w')
        self.createdFlavorFile = open(createdFileName, 'w')

    def close_spider(self, spider):
        self.updatedFlavorFile.close()
        self.createdFlavorFile.close()

    def process_item(self, item, spider):

        if item['isNewFlavor'] == True:
            line = json.dumps(dict(item)) + "\n"
            self.createdFlavorFile.write(line)

        else:
            line = json.dumps(dict(item)) + "\n"
            self.updatedFlavorFile.write(line)

        return item
