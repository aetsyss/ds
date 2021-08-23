# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy

import os
from urllib.parse import urlparse


class LeroyparserPipeline:
    def process_item(self, item, spider):

        # Convert the list of detail names and detail values to a dict.
        item['details'] = dict(zip(item['detail_names'], item['detail_values']))
        item.pop('detail_names', None)
        item.pop('detail_values', None)

        # TODO: Save final item to the data base...

        return item

class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['images']:
            for img in item['images']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['images'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'{item["article"]}/{os.path.basename(request.url)}'
