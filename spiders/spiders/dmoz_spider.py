import scrapy


class DmozSpider(scrapy.Spider):
	"""docstring for DmozSpider"""
	name = "dmoz"
	allowed_domains = ["blog.csdn.net"]
	start_urls = [
		"https://blog.csdn.net/jsjsjs1789/article/details/78602547"
	]

	def parse(self, response):
		print(response.request.headers["User-Agent"])
		links = ''
		link_list = response.xpath("//ul[@class='archive-list']/li/a/@href")
		for link in link_list:
			links += link.extract()
		print(links)
