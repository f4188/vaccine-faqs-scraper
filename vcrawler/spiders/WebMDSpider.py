
import scrapy
from vcrawler.items import FaqItem
from scrapy.http import Request

from urlparse import urlparse
from urlparse import urljoin
import os

class WebMDSpider(scrapy.Spider):
	name = "webmd"
	# allowed_domains = ["https://www.cdc.gov/"]

	#start_urls = ["https://www.cdc.gov/vaccines/vac-gen/common-faqs.htm"]

	def start_requests(self):
		yield scrapy.Request("https://www.webmd.com/children/vaccines/news/20080306/vaccine-faq", self.parse0)

		yield scrapy.Request("https://www.webmd.com/vaccines/adult-immunizations-what-you-need", self.parse0)
		yield scrapy.Request("https://www.webmd.com/vaccines/tetanus-vaccine", self.parse0)
		yield scrapy.Request("https://www.webmd.com/vaccines/hepatitis-a-vaccine-for-adults#1", self.parse0)
		yield scrapy.Request("https://www.webmd.com/vaccines/hpv-vaccine#1", self.parse0)
		yield scrapy.Request("https://www.webmd.com/vaccines/tdap-vaccine-for-adults", self.parse0)
		yield scrapy.Request("https://www.webmd.com/skin-problems-and-treatments/shingles/shingles-vaccine", self.parse0)
		yield scrapy.Request("https://www.webmd.com/vaccines/meningococcal-vaccine-for-adults", self.parse0)
		yield scrapy.Request("https://www.webmd.com/vaccines/adult-mmr-vaccine-guidelines", self.parse0)
		yield scrapy.Request("https://www.webmd.com/vaccines/hepatitis-a-vaccine-for-adults", self.parse0)
		yield scrapy.Request("https://www.webmd.com/hepatitis/hepb-guide/hepatitis-b-prevention", self.parse0)
		yield scrapy.Request("https://www.webmd.com/a-to-z-guides/prevention-15/vaccines/travel-vaccinations", self.parse0)

		yield scrapy.Request("https://www.webmd.com/cold-and-flu/advanced-reading-types-of-flu-viruses", self.parse0)

		yield scrapy.Request("https://www.webmd.com/children/vaccines/immunization-overview", self.parse0)
		yield scrapy.Request("https://www.webmd.com/children/vaccines/default.htm", self.parse1)
		yield scrapy.Request("https://www.webmd.com/children/vaccines/whooping-cough-and-the-dtap-vaccine", self.parse0)
		yield scrapy.Request("https://www.webmd.com/children/vaccines/immunizations-vaccines-power-of-preparation#1", self.parse0)

		yield scrapy.Request("https://www.webmd.com/a-to-z-guides/prevention-15/vaccines/fact-sheet-vaccines", self.parse2)
		yield scrapy.Request("https://www.webmd.com/a-to-z-guides/prevention-15/vaccines/fact-sheet-vaccines?page=2", self.parse2)

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