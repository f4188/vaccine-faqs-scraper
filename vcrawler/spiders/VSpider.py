
import scrapy
from vcrawler.items import FaqItem
from scrapy.http import Request

from urlparse import urlparse
import json
import vcrawler.vaccine as vaccine
import os

class VSpider(scrapy.Spider):
	name = "vspider"

	custom_settings = {
		'DEPTH_LIMIT' : 0,
	}

	def __init__(self, category=None, *args, **kwargs):
		super(VSpider, self).__init__(*args, **kwargs)
		urls = vaccine.getUrlsFromJsonFile('./vcrawler/vaccinefaqs.json')
		self.start_urls = urls
		self.allowed_domains = vaccine.getDomainsFromUrls(urls)

	#def start_requests(self):
	#	yield scrapy.Request(url=datum.url, callback=self.parse)


	def parse(self, response):
		parsed = urlparse(response.url)
		url = parsed.netloc + parsed.path
		filename = ('faqs-%s' % url).replace("/", "_")

		dirname = os.path.dirname(__file__)

		dest_dir = '../../../faqs/' 

		with open(os.path.join(dirname, dest_dir, filename), 'w') as f:
			f.write(response.body)

		self.log('Saved file %s' % filename)

		links = response.xpath('//a/@href').extract()
		crawledLinks = []

		#linkPatterm = re.compile("")

		for link in links:
			#if linkPattern.match(link) and not link in crawledLinks:
			if not link in crawledLinks:
				crawledLinks.append(link)
				yield Request(parsed.scheme + '://' + parsed.netloc + link, self.parse)
