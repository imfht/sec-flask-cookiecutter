# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import requests
import scrapy

api_endpoint = 'http://localhost:5000/api/domains'


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        current_page = 1
        while True:
            resp = requests.get(api_endpoint, params={'page': current_page}).json()
            if not resp['objects']:
                break
            for i in resp['objects']:
                yield scrapy.Request(url=i['domain'])
            current_page += 1

    def parse(self, response):
        title = response.xpath("//title/text()").get()
        self.logger.info("[%s] - %s" % (response.url, title))
