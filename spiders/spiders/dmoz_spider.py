import scrapy
from spiders.items import DmozItem
import redis
import hashlib
from rediscluster import StrictRedisCluster

class DmozSpider(scrapy.Spider):
	"""docstring for DmozSpider"""
	name = "dmoz"
	allowed_domains = ["blog.csdn.net"]
	start_urls = [
		"https://blog.csdn.net/mygodit/article/details/83584149"
	]

	def parse(self, response):
		self.spider_detail(self, response)

	def spider_detail(self, response):
		if self.exitsurl(response.url)=='1':
			link_list = response.xpath("//ul[@class='archive-list']/li/a/@href")
			title = response.xpath("//h1[@class='title-article']/text()").extract()[0]
			url_list=response.xpath("//li[@class='right-item']/a/@href")

			linklist = []
			for link in link_list:
				linklist.append(link.extract())
			item = DmozItem()
			item['title'] = title
			item['link'] = linklist
			yield item
		if
		yield scrapy.Request(url, callback=self.parse(), dont_filter=True)

	def exitsurl(self, url):
		r = redis.Redis(host='localhost', port=6379, decode_responses=True)
		hl = hashlib.md5()
		hl.update(url.encode(encoding='utf-8'))
		md5url = hl.hexdigest()
		print(md5url)
		if r.get(md5url) != '1':
			r.set(md5url, '1')
			return 1
		else:
			# 已经存在该url
			return 0
