# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient

class InstapeoplePipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.instagram

    def process_item(self, item, spider):
        type = item['type']
        item.pop('type', None)

        item['account_id'] = int(item['account_id'])

        collection = self.mongo_base[type]
        collection.insert_one(item)

        return item
