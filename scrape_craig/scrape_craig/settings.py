# Scrapy settings for scrap_craig project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os

BOT_NAME = 'scrape_craig'

SPIDER_MODULES = ['scrape_craig.spiders']
NEWSPIDER_MODULE = 'scrape_craig.spiders'

# scrapy-mongodb settings
MONGODB_URI = os.getenv('MONGOHQ_URL')
MONGODB_DATABASE = 'craig'
MONGODB_COLLECTION = 'postings'
MONGODB_UNIQUE_KEY = 'pid'
MONGODB_STOP_ON_DUPLICATE = 1 # tell the crawler to stop when one duplicate is detected

ITEM_PIPELINES = ['scrapy_mongodb.MongoDBPipeline']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrap_craig (+http://www.yourdomain.com)'
