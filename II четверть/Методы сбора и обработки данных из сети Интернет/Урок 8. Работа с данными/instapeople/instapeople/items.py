# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

def map_account_id(value: str):
    return int(value)

class InstapeopleItem(scrapy.Item):
    account_id = scrapy.Field()
    type = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    full_name = scrapy.Field()
    photo = scrapy.Field()
    _id = scrapy.Field()
