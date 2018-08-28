
import scrapy
from vcrawler.items import FaqItem
from scrapy.http import Request

from urlparse import urlparse
from urlparse import urljoin

from scrapy import Selector
# import json
# import vcrawler.vaccine as vaccine
import os

class HSESpider(scrapy.Spider):
	name = "hse"

	def start_requests(self):
		yield scrapy.Request("https://www.hse.ie/eng/health/immunisation/pubinfo/adult/hepb/hepb.html", self.parse0)
		yield scrapy.Request("https://www.hse.ie/eng/health/immunisation/pubinfo/adult/pneumo/", self.parse0)
		yield scrapy.Request("https://www.hse.ie/eng/health/immunisation/pubinfo/adult/pertussis/", self.parse1)

	def parse0(self, response):
		self.logger.info('Getting faqs from %s', response.url)
		psels = response.xpath('//div[@class="content"]/*')
		faqs = []
		faqi  = []
		for psel in psels:
			if len(psel.xpath('text()').extract()) > 0 and psel.xpath('text()').extract()[0] == u'\xa0':
				continue
			if not psel.xpath('a'):
				faqi.append(psel)
			elif len(faqi) > 0:
				faqs.append(faqi)
				faqi = []

		if len(faqi) > 0: 
			faqs.append(faqi)

		for sels in faqs:
			if not sels[0].xpath('strong/text()'):
				continue
			faqItem = FaqItem()
			faqItem['question'] = sels[0].xpath('strong/text()').extract()[0]
			faqItem['answer'] = ''.join([ ''.join(sel.xpath('.//text()').extract()) for sel in sels if not sel.xpath('strong').extract()])
			faqItem['url'] = response.url
			yield faqItem

	def parse1(self, response):
		self.logger.info('Getting faqs from %s', response.url)

		psels = response.xpath('//div[@class="content"]/*')
		faqs = []
		faqi  = [psels[0]]
		for psel in psels[1:]:
			if len(psel.xpath('text()').extract()) > 0 and psel.xpath('text()').extract()[0] == u'\xa0':
				continue
			if psel.xpath('span'):
				faqs.append(faqi)
				faqi = [psel]
			else:
				faqi.append(psel)

		if len(faqi) > 0: 
			faqs.append(faqi)

		for sels in faqs:
			if not sels[0].xpath('span'):
				continue
			faqItem = FaqItem()
			faqItem['question'] = sels[0].xpath('.//text()').extract()[0]
			faqItem['answer'] = ''.join( [''.join(sel.xpath('.//text()').extract()) for sel in sels[1:] if sel.xpath('.//text()').extract()])
			faqItem['url'] = response.url
			yield faqItem