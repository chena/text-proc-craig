from scrapy.item import Item, Field

class ScrapeCraigItem(Item):
	link = Field()
	title = Field()
	description = Field()
