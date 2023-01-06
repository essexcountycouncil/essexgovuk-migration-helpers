import scrapy
from scrapy.spidermiddlewares.httperror import HttpError


class BaseScraper(scrapy.Spider):
    def parse(self, response):

        try:
            contains_table = bool(response.xpath("//table"))

            yield {
                'url': response.url,
                'contains_table': contains_table,
                'status': response.status,
                'type': 'page'
            }

            for link in self.link_extractor.extract_links(response):
                if "?" not in link.url:
                    yield response.follow(link, callback=self.parse, errback=self.parse_error)
        
        # Handle files
        except scrapy.exceptions.NotSupported:
            yield {
                'url': response.url,
                'status': response.status,
                'type': "file"
            }
    
    def parse_error(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

            yield {
                'url': response.url,
                'status': response.status
            }
