# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline

class HomeWork6Pipeline:
    def __init__(self):
        client = MongoClient('localhost:27017')
        self.mongo_db = client.parser_job



class AdsPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item.get('photos'):
            for ing in item.get('photos'):
                try:
                    yield scrapy.Request(ing)
                except Exception as e:
                    print(e)
    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item


    def process_item(self, item, spider):
        collection = self.mongo_db[spider.name]
        collection.insert_one(item)

        return item