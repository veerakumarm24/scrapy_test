# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo


class ScrapyDumpPipeline:
    collection_name = 'profile_table'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        self.insert_profileTable(item)
        return item

    def gen_auto_inc(self, table_name):
        cur_index = 0
        last_row = self.db[table_name].find({}).sort([("_id", -1)]).limit(1)
        if last_row:
            for obj in last_row:
                cur_index = obj['_id'] if obj['_id'] else 0
        return (cur_index+1)

    def insert_profileTable(self, data):
        id = self.gen_auto_inc(self.collection_name)
        obj = {}
        obj['_id'] = id
        obj['name'] = data['name']
        obj['ratings'] = data['ratings']
        obj['address'] = data['address']
        obj['phone'] = data['phone']
        obj['profileInfo'] = data['profileInfo']
        obj['profileImage'] = data['profileImage']
        obj['speciality'] = data['speciality']
        obj['gender'] = data['gender']
        obj['age'] = data['age']
        profile_id = self.db[self.collection_name].insert(obj)
        self.insert_reviewTable(profile_id, data['reviewItem'])
        logging.debug("profile data added to MongoDB")
        return

    def insert_reviewTable(self, profile_id, data):
        for row in data:
            id = self.gen_auto_inc('review_table')
            obj = dict(row)
            obj['_id'] = id
            obj['profile_id'] = profile_id
            self.db['review_table'].insert(obj)
            logging.debug("review data added to MongoDB")
        return