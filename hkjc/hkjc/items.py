# -*- coding: utf-8 -*-

import scrapy


class HkjcHorseItem(scrapy.Item):
    racenumber = scrapy.Field()
    raceindex = scrapy.Field()
    racename = scrapy.Field()
    horsenumber = scrapy.Field()
    horsename = scrapy.Field()
    horsecode = scrapy.Field()
    timelist = scrapy.Field()
    sirename = scrapy.Field()
    racedate = scrapy.Field()
    place = scrapy.Field()
    final_sec_time = scrapy.Field()
    raceclass = scrapy.Field()
    racedistance = scrapy.Field()
    racegoing = scrapy.Field()
    racetrack = scrapy.Field()
    horsecodelist = scrapy.Field()
    racingincidentreport = scrapy.Field()
