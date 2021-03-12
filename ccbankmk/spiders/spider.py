import scrapy

from scrapy.loader import ItemLoader

from ..items import CcbankmkItem
from itemloaders.processors import TakeFirst


class CcbankmkSpider(scrapy.Spider):
	name = 'ccbankmk'
	start_urls = ['http://www.ccbank.mk/Content.aspx?id=97&lng=1&page=0']

	def parse(self, response):
		post_links = response.xpath('//div[@class="latest-news-container"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="pagination-gallery"]//a[text()="Следна"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		print(response)
		title = response.xpath('//h1[@class="single-news-main-heading2"]/text()').get()
		description = response.xpath('//div[@class="single-news-main-paragraph"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="single-news-main-date"]/text()').get()

		item = ItemLoader(item=CcbankmkItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
