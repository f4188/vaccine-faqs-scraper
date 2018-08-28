
import scrapy
from vcrawler.items import FaqItem
from scrapy.http import Request

from urlparse import urlparse
from urlparse import urljoin
import os

class HealNYSpider(scrapy.Spider):
	name = "healny"
	# allowed_domains = ["https://www.cdc.gov/"]

	#start_urls = ["https://www.cdc.gov/vaccines/vac-gen/common-faqs.htm"]

	def start_requests(self):
		yield scrapy.Request("https://www.health.ny.gov/prevention/immunization/vaccine_safety/frequently_asked_questions.htm", self.parse0)

	def parse0(self, response):

		self.logger.info('Getting faq at %s', response.url)

		# faqItem = FaqItem()
		# ans = []

		for sel in response.xpath('//div[@id="content"]/h2'):

			faqItem = FaqItem()
			faqItem['question'] = sel.xpath('.//text()').extract()[0]
			faqItem['answer'] = sel.xpath('following-sibling::p//text()').extract()[0]

			yield faqItem