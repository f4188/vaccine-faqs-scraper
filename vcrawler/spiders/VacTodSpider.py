
import scrapy
from vcrawler.items import FaqItem
from scrapy.http import Request

from urlparse import urlparse
from urlparse import urljoin
import os

class VacTodSpider(scrapy.Spider):
	name = "vactod"

	def start_requests(self):
		yield scrapy.Request("https://www.vaccinestoday.eu/faq/", self.parse0)

	def parse0(self, response):

		self.logger.info('Getting faq at %s', response.url)
		articles = response.xpath('//article')

		for article in articles:
			if not article.xpath('.//div[@class="faq-duo"]/p/text()').extract():
				continue

			faqItem = FaqItem()
			faqItem['question'] = article.xpath('.//div[@class="faq-duo"]/p/text()').extract()[0]
			url = article.xpath('.//a/@href').extract()[0]
			faqItem['url'] = url
			request = scrapy.Request(url, callback=self.parse1)
			request.meta['item'] = faqItem
			yield request

	def parse1(self, response):
		self.logger.info('Getting faqs from %s', response.url)

		faqItem = response.meta['item']
		faqItem['answer'] = ''.join(response.xpath('//article/div[@class="entry-content"]//text()').extract())
		yield faqItem
