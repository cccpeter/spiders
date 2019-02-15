import scrapy
from spiders.items import DmozItem
import redis
import hashlib
import time
import random

class DmozSpider(scrapy.Spider):
	"""docstring for DmozSpider"""
	name = "dmoz"
	allowed_domains = ["blog.csdn.net"]
	start_urls = [
		"https://blog.csdn.net/dd864140130/article/details/49817357"
	]

	def parse(self, response):
		# print('__________________负责解析数据item__________________')
		# 爬取该文章的左下角归档的文章记录
		link_list = response.xpath("//ul[@class='archive-list']/li/a/@href")
		for link in link_list:
			# 进入文章的归档列表
			time.sleep(0.1)
			yield scrapy.Request(link.extract(), callback=self.parse_detail, dont_filter=True)

	def parse_detail(self, response):
		page_link = response.xpath("//div[@class='article-item-box csdn-tracking-statistics']/h4/a/@href").extract()
		# 各个文章的地址
		if self.exitsurl(response.url) != '0':
			del(page_link[0])
			for page in page_link:
				# print('获取到文章的url:' + page)
				#开始解析文章内容
				time.sleep(0.2)
				yield scrapy.Request(page, callback=self.resolve_page, dont_filter=True)
			# print(response.xpath("//html"))
	# 解析文章

	def resolve_page(self, response):
		if self.exitsurl(response.url) != '0':
			title = response.xpath("//h1[@class='title-article']/text()").extract()[0]
			original = response.xpath("//span[@class='count']/text()").extract()[0]
			fans = response.xpath("//span[@class='count']/text()").extract()[1]
			likes = response.xpath("//span[@class='count']/text()").extract()[2]
			comment = response.xpath("//span[@class='count']/text()").extract()[3]
			# content = response.xpath("//div[@class='htmledit_views']").extract()[0]
			data = response.xpath("//span[@class='time']").extract()[0]
			author = response.xpath("//a[@class='follow-nickName']/text()").extract()[0]
			readnum = response.xpath("//span[@class='read-count']/text()").extract()[0]
			readnum=readnum.replace("阅读数：", "")
			# print("日期："+data)
			# print("作者："+author)
			# print("阅读数:"+readnum)
			# print("原创:"+original)
			# print("粉丝:"+fans)
			# print("喜欢:"+likes)
			# print("评论数量:"+comment)
			# print("内容:"+content)
			item = DmozItem()
			item['title'] = title
			item['link'] = response.url
			item['author'] = author
			item['data'] = data
			item['readnum'] = readnum
			item['fans'] = fans
			item['likes'] = likes
			item['comment'] = comment
			print('爬取的连接为:'+response.url)
			time.sleep(0.1)
			yield item
			page_list = response.xpath("//div[@class='content']/a/@href").extract()
			for page in page_list:
				yield scrapy.Request(page, callback=self.parse, dont_filter=True)
		else:
			print('已经存在，则不爬')

	def exitsurl(self, url):
		r = redis.Redis(host='localhost', port=6379, decode_responses=True)
		hl = hashlib.md5()
		hl.update(url.encode(encoding='utf-8'))
		md5url = hl.hexdigest()
		# print(md5url)
		if r.get(md5url) != '1':
			r.set(md5url, '1')
			print('文章不存在')
			return '1'
		# 不存在该文章
		else:
			# 已经存在该url
			print('文章存在，不爬取')
			return '0'

	# '''过滤HTML中的标签
	# #将HTML中标签等信息去掉
	# #@param htmlstr HTML字符串.'''
	#
	# def filter_tag(self, htmlstr):
	# 	re_cdata = re.compile('<!DOCTYPE HTML PUBLIC[^>]*>', re.I)
	# 	re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # 过滤脚本
	# 	re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # 过滤style
	# 	re_br = re.compile('<br\s*?/?>')
	# 	re_h = re.compile('</?\w+[^>]*>')
	# 	re_comment = re.compile('<!--[\s\S]*-->')
	# 	s = re_cdata.sub('', htmlstr)
	# 	s = re_script.sub('', s)
	# 	s = re_style.sub('', s)
	# 	s = re_br.sub('\n', s)
	# 	s = re_h.sub(' ', s)
	# 	s = re_comment.sub('', s)
	# 	blank_line = re.compile('\n+')
	# 	s = blank_line.sub('\n', s)
	# 	s = re.sub('\s+', ' ', s)
	# 	s = self.replaceCharEntity(s)
	# 	return s
	#
	# def replaceCharEntity(self, htmlstr):
	# 	CHAR_ENTITIES = {'nbsp': '', '160': '',
	# 					 'lt': '<', '60': '<',
	# 					 'gt': '>', '62': '>',
	# 					 'amp': '&', '38': '&',
	# 					 'quot': '"''"', '34': '"'}
	# 	re_charEntity = re.compile(r'&#?(?P<name>\w+);')  # 命名组,把 匹配字段中\w+的部分命名为name,可以用group函数获取
	# 	sz = re_charEntity.search(htmlstr)
	# 	while sz:
	# 		# entity=sz.group()
	# 		key = sz.group('name')  # 命名组的获取
	# 		try:
	# 			htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)  # 1表示替换第一个匹配
	# 			sz = re_charEntity.search(htmlstr)
	# 		except KeyError:
	# 			htmlstr = re_charEntity.sub('', htmlstr, 1)
	# 			sz = re_charEntity.search(htmlstr)
	# 	return htmlstr