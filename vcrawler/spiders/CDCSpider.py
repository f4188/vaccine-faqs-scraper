
import scrapy
from vcrawler.items import FaqItem
from scrapy.http import Request

from urlparse import urlparse
from urlparse import urljoin
import os

#CDCSpider
'''CDCParsers = [
	{ 
		url : "https://www.cdc.gov/vaccines/vac-gen/common-faqs.htm",
		parse0 : lambda self, response:  
		 
	},
	{ url : "https://www.cdc.gov/vaccines/parents/parent-questions.html", self.parse2) },
	{ url : "https://www.cdc.gov/vaccinesafety/caregivers/faqs.html", self.parse3) },
	{ url : "https://www.cdc.gov/flu/faq/index.htm", self.parse4) } ,
	{ url : "https://www.cdc.gov/meningitis/" },
]'''

class CDCSpider(scrapy.Spider):
	name = "cdc"
	# allowed_domains = ["https://www.cdc.gov/"]

	#start_urls = ["https://www.cdc.gov/vaccines/vac-gen/common-faqs.htm"]

	def start_requests(self):
		yield scrapy.Request("https://www.cdc.gov/vaccines/vac-gen/common-faqs.htm", self.parse0)
		yield scrapy.Request("https://www.cdc.gov/vaccines/parents/parent-questions.html", self.parse2)
		yield scrapy.Request("https://www.cdc.gov/vaccinesafety/caregivers/faqs.html", self.parse3)
		yield scrapy.Request("https://www.cdc.gov/flu/faq/index.htm", self.parse4)
		yield scrapy.Request("https://www.cdc.gov/meningitis/", self.parse6)

	def parse0(self, response):

		self.logger.info('Getting faq at %s', response.url)
		paths = response.xpath('//div[@class="syndicate"]//ul//a/@href').extract()

		for path in paths:
			url = urljoin(response.url, path)
			request = scrapy.Request(url, callback=self.parse1)
			yield request

	def parse1(self, response):
		self.logger.info('Getting faqs from %s', response.url)

		for sel in response.xpath('//div[@class="syndicate"]/h4'):
			faqItem = FaqItem()
			faqItem['question'] = ''.join(sel.xpath('.//text()').extract())
			faqItem['answer'] = ''.join(sel.xpath('following-sibling::div//text()').extract())
			faqItem['url'] = response.url
			yield faqItem

	def parse2(self, response):
		self.logger.info('Getting faqs from %s', response.url)

		for sel in response.xpath('//div[@class="syndicate"]/h3'):
			faqItem = FaqItem()
			faqItem['question'] = ''.join(sel.xpath('.//text()').extract())
			faqItem['answer'] = ''.join(sel.xpath('following-sibling::div//text()').extract())
			faqItem['url'] = response.url
			yield faqItem

	def parse3(self, response):
		self.logger.info('Getting faqs from %s', response.url)

		for sel in response.xpath('//div[@class="syndicate"]//h2'):
			faqItem = FaqItem()
			faqItem['question'] = ''.join(sel.xpath('.//text()').extract())
			faqItem['answer'] = ''.join(sel.xpath('following-sibling::p//text()').extract())
			faqItem['url'] = response.url
			yield faqItem

	def parse4(self, response):

		self.logger.info('Getting faq at %s', response.url)
		paths = response.xpath('//div[@class="syndicate"]//ul//a/@href').extract()

		for path in paths:
			url = urljoin(response.url, path)
			request = scrapy.Request(url, callback=self.parse5)
			yield request

	def parse5(self, response):
		self.logger.info('Getting faqs from %s', response.url)

		for sel in response.xpath('//div[@class="syndicate"]/h3'):
			faqItem = FaqItem()
			faqItem['question'] = ''.join(sel.xpath('.//text()').extract())
			faqItem['answer'] = ''.join(sel.xpath('following-sibling::*//text()').extract())
			faqItem['url'] = response.url
			yield faqItem

	def parse6(self, response):

		self.logger.info('Getting faq at %s', response.url)
		paths = response.xpath('//div[@id="contentArea"]//ul//a/@href').extract()

		for path in paths:
			if path[0] is "h":
				continue
			url = urljoin(response.url, path)
			request = scrapy.Request(url, callback=self.parse7)
			yield request

	def parse7(self, response):
		self.logger.info('Getting faqs from %s', response.url)

		print(response.url)

		for sel in response.xpath('//div[@class="syndicate"]//*[self::h2 or self::h3 or self::h4 or self::h5]'):
			faqItem = FaqItem()

			#ques = '.'.join(sel.xpath('.//text()').extract())
			#if  == ques == ""
			faqItem['question'] = ''.join(sel.xpath('.//text()').extract())

			im_siblings = []
			for sibling in sel.xpath('following-sibling::*'):
				if(sibling.xpath('ancestor-or-self::*[self::h2 or self::h3 or self::h4 or self::h5]')):
					break
				im_siblings.append(''.join(sibling.xpath('.//text()').extract()))

			faqItem['answer'] = ''.join(im_siblings)
			faqItem['url'] = response.url

			yield faqItem