
import scrapy
from vcrawler.items import FaqItem
from scrapy.http import Request

from urlparse import urlparse
from urlparse import urljoin
import os

class EvdaHealSpider(scrapy.Spider):
	name = "evdaheal"

	def start_requests(self):
		yield scrapy.Request("https://www.everydayhealth.com/infant-immunization/faqs-about-childhood-vaccines.aspx", self.parse0)

	def parse0(self, response):

		self.logger.info('Getting faq at %s', response.url)

		for p in response.xpath('//div[@class="article-body"]/*'):

			if not p.xpath('strong'):
				continue

			faqItem = FaqItem()
			faqItem['question'] = ''.join(p.xpath('.//text()').extract())

			im_siblings = []
			for sibling in p.xpath('following-sibling::*'):
				if(sibling.xpath('strong')):
					break
				im_siblings.append(''.join(sibling.xpath('.//text()').extract()))

			faqItem['answer'] = ''.join(im_siblings)
			faqItem['url'] = response.url

			yield faqItem