# -*- coding: utf-8 -*-

# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

ITEM_PIPELINES = {
#        'crawler.pipelines.ScrapPipeline': 300
}
DOWNLOADER_MIDDLEWARES = {
	'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware' : 500
}
HTTPCACHE_ENABLED = True
HTTPCACHE_DIR='/tmp/httpcache'
#HTTPCACHE_STORAGE = 'scrapy.contrib.httpcache.DbmCacheStorage'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawler (+http://www.yourdomain.com)'
