
import scrapy
from vcrawler.items import FaqItem
from scrapy.http import Request

from urlparse import urlparse
from urlparse import urljoin
import os

class ImmNevSpider(scrapy.Spider):
	name = "immnev"

	def start_requests(self):
		yield scrapy.Request("https://immunizenevada.org/faqs", self.parse0)

	def parse0(self, response):

		self.logger.info('Getting faq at %s', response.url)

		for div in response.xpath('//body/div[@id="mainWrapper"]'):
			print(div)

		for sel in response.xpath('//body/div[@id="mainWrapper"]//div[@id="content"]//li'):
			print(sel)
			faqItem = FaqItem()
			faqItem['question'] = sel.xpath('.//text()').extract()[0]

			path = sel.xpath('a/@href').extract()

			faqItem['answer'] = sel.xpath('//p[@id="' + path + '"]/text()').extract()[0]

			yield faqItem