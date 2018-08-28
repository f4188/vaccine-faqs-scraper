# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from vcrawler.items import FaqItem
import json

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        # self.file = open('items.jl', 'r+')
        with open('items.json', 'r+') as f:
        	try:
        		self.data = json.load(f)
        	except ValueError:
        		self.data = dict()
      		self.data[spider.name] = []

    def close_spider(self, spider):
        # self.file.close()
        with open('items.json', 'w') as f:
        	f.write(json.dumps(self.data))

    def process_item(self, item, spider):
    	#d_item = dict(item)
    	#d_item["spider_name"] = spider.name
        # line = json.dumps(d_item) + "\n"
        # self.file.write(line)
        if not self.data[spider.name]:
        	self.data[spider.name] = []
        self.data[spider.name].append(dict(item))
        return item

class VcrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):

	collection_name = 'scrapy_items'

	def __init__(self, mongo_uri, mongo_db):
		self.mongo_uri = mongo_uri
		self.mongo_db = mongo_db

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			mongo_uri=crawler.settings.get('MONGO_URI'),
			mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
		)

	def open_spider(self, spider):
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]

	def close_spider(self, spider):
		self.client.close()

	def process_items(self, item, spider):
		self.db[self.collection_name].insert_one(dict(item))
		return item