# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ExamItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    招生单位 = scrapy.Field()
    院系所 = scrapy.Field()
    专业 = scrapy.Field()
    研究方向 = scrapy.Field()
    拟招人数 = scrapy.Field()
    考试方式 = scrapy.Field()
    跨专业 = scrapy.Field()
    学习方式 = scrapy.Field()
    指导老师 = scrapy.Field()
    政治 = scrapy.Field()
    外语 = scrapy.Field()
    业务课一 = scrapy.Field()
    业务课二 = scrapy.Field()
    pass
