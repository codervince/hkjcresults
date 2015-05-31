# -*- coding: utf-8 -*-

# Scrapy settings for hkjc project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'hkjc'

SPIDER_MODULES = ['hkjc.spiders']
NEWSPIDER_MODULE = 'hkjc.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hkjc (+http://www.yourdomain.com)'

DUPEFILTER_CLASS = 'hkjc.utils.CustomFilter'
