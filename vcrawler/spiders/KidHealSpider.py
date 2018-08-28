
import scrapy
from vcrawler.items import FaqItem
from scrapy.http import Request

from urlparse import urlparse
from urlparse import urljoin
import os

class KidHealSpider(scrapy.Spider):
	name = "kidheal"

	def start_requests(self):
		yield scrapy.Request("https://kidshealth.org/en/parents/fact-myth-immunizations.html", self.parse0)

	def parse0(self, response):

		self.logger.info('Getting faq at %s', response.url)

		for sel in response.xpath('//div[@id="khcontent_article"]//*[self::h3]'):
			faqItem = FaqItem()

			faqItem['question'] = ''.join(sel.xpath('.//text()').extract())

			im_siblings = []
			for sibling in sel.xpath('following-sibling::*'):
				if(sibling.xpath('ancestor-or-self::*[self::h3]')):
					break
				im_siblings.append(''.join(sibling.xpath('.//text()').extract()))

			faqItem['answer'] = ''.join(im_siblings)
			faqItem['url'] = response.url

			yield faqItem