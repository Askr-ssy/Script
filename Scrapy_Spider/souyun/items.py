# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SouyunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    #一个容器是一篇典故，包括其下所有出处
    #涉及人物与Url与数量
    Author=scrapy.Field()
    AuthorUrl=scrapy.Field()
    AuthorCount=scrapy.Field()

    #典故名称
    StoryNumber=scrapy.Field()
    StoryName=scrapy.Field()
    StoryReName=scrapy.Field()
    
    #典故正体 dict
    Story=scrapy.Field()

    #典故简释与例句
    Poetry=scrapy.Field()
    Poet=scrapy.Field()
    PoetryTitle=scrapy.Field()
    pass
