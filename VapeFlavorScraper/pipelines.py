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
import urllib
import re

from scrapy.utils.project import get_project_settings


class DefaultValuesPipeline(object):
    def process_item(self, item, spider):
        item['failed'] = False
        item['isNewFlavor'] = True
        return item

class ItemDropPipeline(object):

    drop_strings = [
        '- Choose any 10 x 28.5ml of our Intense Flavours',
        '- Choose any 5 x 28.5ml of our Intense Flavours',
        '- Choose any 50 x 28.5ml of our Intense Flavours',
        '- Choose any 6  x 28.5ml of our Intense Flavours',
        '- Choose any 8 x 28.5ml of our Intense Flavours',
        '- Choose any 20 x 28.5ml of our Intense Flavours',
        '- Choose any 15 x 28.5ml of our Intense Flavours',
        '- Choose any 12 x 28.5ml of our Intense Flavours',
        'Strawberry Intense Flavour Range Food Flavours 100ml',
        '0-Twist-Open Dispensing Cap'
    ]

    def process_item(self, item, spider):
        name = item['name']

        for drop in self.drop_strings:
            if drop == name:
                raise DropItem("Dropping Bad item: %s" % item)

        return item

class NameProcessingPipeline(object):

    remove_strings = [
        'Intense Flavour Range Food Flavourings 28.5ml',
        'Intense Flavour Range Food Flavourimgs 28.5ml',
        'Intense Flavour Range Food Flavouring 28.5ml',
        'Intense Flavour Range Food Flavours 28.5ml',
        'Intense Flavour Food Flavourings 28.5ml',
        'Flavouring Intense Flavour Range 28.5ml',
        'Intense Flavour Range Food Flavours',
        'Intense Flavour Range Food Flavourings 100ml',
        'Ntense Flavour Range Food Flavourings 28.5ml',
        'Intense Flavour Range Food Flavourings 2.5ml',
        'Intense Flavour Range Food Flavourings',
        'Ntense Flavour Range Food Flavourings 28.5ml',
        'Intense Flavour Range Food Flavouring',
        'Ntense Flavour Range Food Flavourings 28.5Ml',
        'ntense Flavour Range Food Flavourings 28.5ml',
        'Flavor Concentrate',
        'Flavoring',
        'Flavor',
        '1 dram',
        '1  oz.',
        'W.S.',
        '100Ml',
        'DSV',
        '140ml',
        '3ml',
        '30ml',
        '10ml',
        'Liquid',
        'FPF',
        '\(MB\)'
    ]

    def process_item(self, item, spider):
        name = item['name']

        for replace in self.remove_strings:
            name = re.sub(r'%s' % replace , '' , name ).strip()

        name = name.lower().title()
        item['name'] = name
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

class DescriptionPipeline(object):

    def process_item(self, item, spider):

        if item['description'] == '':
            item['description'] = item['name']
            return item

        if isinstance( item['description'] , list ):

            if( len(item['description']) == 0 ):
                item['description'] = item['name']

            else:
                item['description'] = item['description'][0]
                return item

        return item

class ImagePipeline(object):

    def process_item(self, item, spider):

        if isinstance( item['image_url'] , list ):

            if( len(item['image_url']) == 0 ):
                item['image_url'] = ''
                return item

            else:
                item['image_url'] = item['image_url'][0]
                return item
        else:
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
            return item

        #setup the JSON payload
        payload = {'name': item['name'], 'description': item['description'], 'image_url': item['image_url'] , 'manufacturer': item['manufacturer'], 'link': item['link']}

        #setup up the request headers for Authorization
        headers = {'Authorization' : self.token}

        #setup the flavor get URL where we will check if this flavor already exists
        name = item['name'].replace( '&' , '%26' )
        flavorGetURL = self.url + '/flavor?manufacturer='+ item['manufacturer']  + '&name=' + name

        #check for the current flavor already in the database
        res = requests.get( flavorGetURL , headers=headers )

        #if the request failed (404) then mark the item as failed
        if res.status_code is not 200:
            item['failed'] = True
            return item

        #if the flavor is already in the database, then we will just do an update with any new data
        if len( res.json() ) is not 0:
            flavorId = res.json()[0]['id']
            flavorPutURL = self.url + '/flavor/' + str(flavorId)
            item['isNewFlavor'] = False
            res = requests.put( flavorPutURL , headers=headers , data=payload )

            if res.status_code is not 200:
                item['failed'] = True
                logging.info( "Item Failed: " + item['name'] )
                return item

            else:
                logging.info( "Updated Item: " + item['name'] )

        #otherwise we will create a new flavor in the database
        else:
            flavorPutURL = self.url + '/flavor'
            res = requests.post( flavorPutURL , headers=headers , data=payload )

            if res.status_code is not 201:
                item['failed'] = True
                logging.info( "Item Failed: " + item['name'] )
                return item

            else:
                item['isNewFlavor'] = True
                logging.info( "Created Item: " + item['name'] )

        item['failed'] = False
        return item

class JsonWriterPipeline(object):

    def open_spider(self, spider):

        timeString = time.strftime( "%Y-%m-%dT%H-%M-%S" , time.localtime() )
        updatedFileName = "data/%s/Updated_%s.json" % (spider.name , timeString )
        createdFileName = "data/%s/Created_%s.json" % (spider.name , timeString )
        failedFileName = "data/%s/Failed_%s.json" % (spider.name , timeString )
        self.updatedFlavorFile = open(updatedFileName, 'w')
        self.createdFlavorFile = open(createdFileName, 'w')
        self.failedFlavorFile = open(failedFileName, 'w')

    def close_spider(self, spider):
        self.updatedFlavorFile.close()
        self.createdFlavorFile.close()
        self.failedFlavorFile.close()

    def process_item(self, item, spider):

        if item['failed'] is True:
            line = json.dumps(dict(item)) + "\n"
            self.failedFlavorFile.write(line)
            return item

        if item['isNewFlavor'] == True:
            line = json.dumps(dict(item)) + "\n"
            self.createdFlavorFile.write(line)

        else:
            line = json.dumps(dict(item)) + "\n"
            self.updatedFlavorFile.write(line)

        return item
