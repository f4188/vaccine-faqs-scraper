
import scrapy
from vcrawler.items import FaqItem
from scrapy.http import Request

from urlparse import urlparse
from urlparse import urljoin
import os

class MedNetSpider(scrapy.Spider):
	name = "mednet"

	def start_requests(self):
		yield scrapy.Request("https://www.medicinenet.com/vaccination_faqs/article.htm#why_do_people_need_vaccines_what_is_immunization_what_is_immunity", self.parse0)

	def parse0(self, response):

		self.logger.info('Getting faq at %s', response.url)

		for sel in response.xpath('//div[@id="pageContainer"]/div[@class="apPage"]/div[@class="wrapper"]'):
			print(sel)
			faqItem = FaqItem()
			faqItem['question'] = ''.join(sel.xpath('div/h3//text()').extract())

			im_siblings = []
			for sibling in sel.xpath('div[1]/following-sibling::*'):
				im_siblings.append(''.join(sibling.xpath('.//text()').extract()))

			faqItem['answer'] = ''.join(im_siblings)
			faqItem['url'] = response.url

			yield faqItem