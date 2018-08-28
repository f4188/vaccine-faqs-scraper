
import scrapy
from vcrawler.items import FaqItem
from scrapy.http import Request

from urlparse import urlparse
from urlparse import urljoin
import os

class NVICSpider(scrapy.Spider):
	name = "nvic"
	# allowed_domains = ["https://www.cdc.gov/"]

	#start_urls = ["https://www.cdc.gov/vaccines/vac-gen/common-faqs.htm"]

	def start_requests(self):
		yield scrapy.Request("https://www.webmd.com/children/vaccines/news/20080306/vaccine-faq", self.parse0)


	def parse1(self, response):

		self.logger.info('Getting faq at %s', response.url)

		for url in response.xpath('//ul[@class="long-list"]/li/a/@href').extract():
			request = scrapy.Request(url, callback=self.parse0)
			yield request


	def parse0(self, response):

		self.logger.info('Getting faq at %s', response.url)

		for sel in response.xpath('//div[@class="article-body"]//section'):
			if not sel.xpath('h2'):
				continue
			faqItem = FaqItem()
			faqItem['question'] = sel.xpath('h2/text()').extract()[0]
			faqItem['answer'] = ''.join(sel.xpath('p/text()').extract())
			faqItem['url'] = response.url
			yield faqItem


	def parse2(self, response):

		self.logger.info('Getting faq at %s', response.url)

		for sel in response.xpath('//div[@class="article-content"]//section'):
			if not sel.xpath('h3'):
				continue
			faqItem = FaqItem()
			faqItem['question'] = sel.xpath('h3/text()').extract()[0]
			faqItem['answer'] = ''.join(sel.xpath('*[not(self::h3)]/text()').extract())
			faqItem['url'] = response.url
			yield faqItem