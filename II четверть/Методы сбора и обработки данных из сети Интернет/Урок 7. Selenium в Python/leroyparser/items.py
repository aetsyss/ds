# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def map_price(price: str):
    """ Convert string price to integer """
    try:
        return int(price.replace(' ', ''))
    except:
        return str

def map_image(image: str):
    """ Convert image url to higher resolution """
    return image.replace('w_82,h_82', 'w_500,h_500')

def map_detail_values(value: str):
    return " ".join(value.split())

class LeroyparserItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    article = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(map_price), output_processor=TakeFirst())
    images = scrapy.Field(input_processor=MapCompose(map_image))
    detail_names = scrapy.Field()
    detail_values = scrapy.Field(input_processor=MapCompose(map_detail_values))
    details = scrapy.Field()
