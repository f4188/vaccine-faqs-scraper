
import scrapy
from vcrawler.items import FaqItem
from scrapy.http import Request

from urlparse import urlparse
from urlparse import urljoin
import os

class ImmFWSpider(scrapy.Spider):
	name = "immfw"  
	def start_requests(self):
		yield scrapy.Request("http://immunizationforwomen.org/providers/diseases-vaccines/measles-mumps-rubella/faqs.php", self.parse0)

	def parse0(self, response):

		self.logger.info('Getting faq at %s', response.url)

		for p in response.xpath('//div[@class="body unit size3of4"]//p'):

			print(p)

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