# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


#receive an item perform an action over it, cleans, duplicates, validation, database
#returns an item or throws DropItem
class HkjcPipeline(object):

	##constants
	

    def process_item(self, item, spider):
        return item
