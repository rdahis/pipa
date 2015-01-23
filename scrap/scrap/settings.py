# -*- coding: utf-8 -*-

# Scrapy settings for scrap project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrap'

SPIDER_MODULES = ['scrap.spiders']
NEWSPIDER_MODULE = 'scrap.spiders'

ITEM_PIPELINES = {
#        'scrap.pipelines.ScrapPipeline': 300
}
DOWNLOADER_MIDDLEWARES = {
	'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware' : 500
}
HTTPCACHE_ENABLED = True
HTTPCACHE_DIR='/tmp/httpcache'
#HTTPCACHE_STORAGE = 'scrapy.contrib.httpcache.DbmCacheStorage'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrap (+http://www.yourdomain.com)'
