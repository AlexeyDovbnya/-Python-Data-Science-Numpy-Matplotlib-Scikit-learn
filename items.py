# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose

def process_name(inf):
    product_name = ''
    if inf:
        product_name = ' '.join(inf[0].split())
    return {'product_name': product_name}

def process_price(value):
    money = 0
    currency = ''
    measure = ''
    if value:
        money = int(value[0].replace(' ', ''))
        currency = value[1]
        measure = value[2]
    return {'money': money, 'currency': currency, 'measure': measure}



class HomeWork6Item(scrapy.Item):
    name = scrapy.Field(input_processor=Compose(process_name))
    price = scrapy.Field(input_processor=Compose(process_price))
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())