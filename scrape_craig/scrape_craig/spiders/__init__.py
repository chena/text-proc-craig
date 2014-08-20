from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from scrape_craig.items import ScrapeCraigItem
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
import re
from datetime import datetime

class CraigSpider(CrawlSpider):
	name = 'craig'
	allowed_domains = ['craigslist.org']
	# scrape the first 10 pages = 1000 items
	start_urls = ['https://newyork.craigslist.org/sub/index%s.html' % (p * 100) for p in range(0, 10)]
	# start_urls = ['https://newyork.craigslist.org/sub']

	rules = (
        # extract links for each posting, and follow links from them
        Rule(LinkExtractor(restrict_xpaths=('//span[@class="pl"]')), follow=True),
    )
	
	url_prefix = 'https://newyork.craigslist.org'

	def parse(self, response):
		urls = response.xpath('//span[@class="pl"]//a/@href').extract()
		for url in urls:
			yield Request(self.url_prefix + url, callback=self.parse_item)

	def parse_item(self, response):
		url = response.url

		item = ScrapeCraigItem()
		item['link'] = url
		item['pid'] = re.search('/(\d+).html', url).group(1)
		
		title = response.xpath('//h2[@class="postingtitle"]/text()').extract()
		# remove as much whitespace as possible
		item['title'] = ' '.join([t.strip() for t in title]).strip()
		
		body = response.xpath('//section[@id="postingbody"]/text()').extract()
		item['description'] = ' '.join([b.strip() for b in body]).strip()
		item['created_at'] = datetime.now()
		
		# TODO: extract price? location?
		yield item