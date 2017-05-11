# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class XesItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ID =Field()
    subject =Field()
    grade =Field()
    title =Field()
    day_time=Field()
    begin_time =Field()
    end_time =Field()
    teacher =Field()
    assistant_teacher =Field()
    rank_places =Field()
    price =Field()
    live =Field()
    target =Field()
    available =Field()
    desc=Field()


