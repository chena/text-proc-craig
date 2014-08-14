# Scrapy settings for scrap_craig project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrape_craig'

SPIDER_MODULES = ['scrape_craig.spiders']
NEWSPIDER_MODULE = 'scrape_craig.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrap_craig (+http://www.yourdomain.com)'