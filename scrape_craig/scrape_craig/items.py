from scrapy.item import Item, Field

class ScrapeCraigItem(Item):
	pid = Field() # pid used as PK in the database
	link = Field()
	title = Field()
	description = Field()
	created_at = Field()
