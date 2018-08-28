
import scrapy
from vcrawler.items import FaqItem
from scrapy.http import Request

from urlparse import urlparse
from urlparse import urljoin
import os
import json

class QuoraSpider(scrapy.Spider):
	name = "quora"
	# allowed_domains = ["https://www.cdc.gov/"]

	#start_urls = ["https://www.cdc.gov/vaccines/vac-gen/common-faqs.htm"]

	def __init__(self, category=None, *args, **kwargs):
		super(QuoraSpider, self).__init__(*args, **kwargs)
		
		with open('../quoracrawler/quora.json', 'r') as f:
			self.start_urls = json.load(f).keys()

		#urls = vaccine.getUrlsFromJsonFile('./vcrawler/vaccinefaqs.json')
		
		#self.start_urls = urls
		#self.allowed_domains = vaccine.getDomainsFromUrls(urls)
	#def start_requests(self):
		#yield scrapy.Request("https://www.webmd.com/children/vaccines/news/20080306/vaccine-faq", self.parse0)

	def parse(self, response):

		self.logger.info('Getting faq at %s', response.url)

		faqItem = FaqItem()
		faqItem['question'] = response.xpath('//div[@class="question_qtext"]//span[@class="rendered_qtext"]/text()').extract()[0]
		faqItem['answer'] = response.xpath('//div[@class="ui_qtext_expanded"]')[0].xpath('//text()').extract()
		
		print(faqItem)