
import sys
import json
from urlparse import urlparse

def getUrlsFromJson(data):
	urls = []
	for datum in data:
		urls.append(datum["url"])
	return urls

def getUrlsFromJsonFile(filename):
	with open(filename, 'r') as json_file:
		data = json.load(json_file)
		urls = getUrlsFromJson(data)
		return urls

def getDomainsFromUrls(urls):
	domains = set()
	for url in urls:
		domain = urlparse(url).netloc
		domains.add(domain)
	return list(domains)

if __name__ == '__main__':
	url_json_filename = sys.argv[1]
	urls = getUrlsFromJsonFile(url_json_filename)
	print(urls)