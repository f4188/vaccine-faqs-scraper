
import scrapy
from vcrawler.items import FaqItem
from scrapy.http import Request

from urlparse import urlparse
from urlparse import urljoin
import os

import io
import pdfquery


class MhplanSpider(scrapy.Spider):
	name = "mhplan"  

	start_urls = [
		"https://corp.mhplan.com/ContentDocuments/default.aspx?x=tQBOLpsBu4/gRctYpBXHnB/ppd+PU1SFi+xL6Teftaw/CuN+u7czFtlu3MvfBDL653jOPn64B5yqsIwWX0w03Q=="
	]
	#def start_requests(self):
	#	yield scrapy.Request("https://corp.mhplan.com/ContentDocuments/default.aspx?x=tQBOLpsBu4/gRctYpBXHnB/ppd+PU1SFi+xL6Teftaw/CuN+u7czFtlu3MvfBDL653jOPn64B5yqsIwWX0w03Q==", self.parse0)

	def parse(self, response):

		self.logger.info('Getting faq at %s', response.url)

		#print(dir(response.body))
		#return
		data = io.BytesIO()
		data.write(response.body)
		#with open('./tmp.pdf', 'w') as f:
		#	f.write(response.body)

		# with open('tmp.pdf', 'r') as f:

		# input = open('./tmp.pdf', 'r')
		pdf = pdfquery.PDFQuery(data)
		#pdf = pdfquery.PDFQuery("./tmp.pdf")
		pdf.load()
		text = pdf.tree.xpath('//LTTextLineHorizontal//text()')
		print(text)

		faqItem = FaqItem()
		#faqItem['answer'] = ''.join(im_siblings)
		#aqItem['url'] = response.url

		yield faqItem