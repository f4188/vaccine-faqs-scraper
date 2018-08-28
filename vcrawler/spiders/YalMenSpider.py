
import scrapy
from vcrawler.items import FaqItem
from scrapy.http import Request

from urlparse import urlparse
from urlparse import urljoin
import os

class YalMenSpider(scrapy.Spider):
	name = "yalmen"
	# allowed_domains = ["https://www.cdc.gov/"]

	#start_urls = ["https://www.cdc.gov/vaccines/vac-gen/common-faqs.htm"]

	def start_requests(self):
		yield scrapy.Request("https://emergency.yale.edu/meningitis-faq", self.parse0)

	def parse0(self, response):

		self.logger.info('Getting faq at %s', response.url)

		faqItem = FaqItem()
		ans = []

		for sel in response.xpath('//p[@class="body"]'):

			if sel.xpath('.//strong'):
				if len(ans) > 0:
					faqItem['answer'] = ''.join(ans)
					yield faqItem
				ans = []
				faqItem['question'] = sel.xpath('.//strong/text()').extract()
			else:
				ans.append(''.join(sel.xpath('.//text()').extract()))
