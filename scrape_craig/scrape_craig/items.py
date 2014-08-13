from scrapy.item import Item, Field

class ScrapeCraigItem(Item):
	pid = Field()
	title = Field()
	link = Field()
	description = Field()
