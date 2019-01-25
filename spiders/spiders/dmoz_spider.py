import scrapy
from spiders.items import DmozItem

class DmozSpider(scrapy.Spider):
	"""docstring for DmozSpider"""
	name = "dmoz"
	allowed_domains = ["blog.csdn.net"]
	start_urls = [
		"https://blog.csdn.net/jsjsjs1789/article/details/78602547"
	]

	def parse(self, response):
		print(response.request.headers["User-Agent"])
		link_list = response.xpath("//ul[@class='archive-list']/li/a/@href")
		title = response.xpath("//h1[@class='title-article']/text()").extract()[0]
		linklist = []
		for link in link_list:
			linklist.append(link.extract())
		item = DmozItem()
		item['title'] = title
		item['link'] = linklist
		yield item
