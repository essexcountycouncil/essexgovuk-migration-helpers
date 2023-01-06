import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from urllib.parse import urlparse

from constants import CONTENTFUL_BASE_URL, MIGRATION_TEST_DOMAIN

class BaseScraper(scrapy.Spider):
    def start_requests(self):
        """Override scrapy's defaults to call parse_error for start_urls that error"""
        for u in self.start_urls:
            yield scrapy.Request(u, errback=self.parse_error)

    def parse(self, response):

        try:
            contains_table = bool(response.xpath("//table"))

            error = ""
            
            # Flag urls where the slug has not migrated correctly
            # Incorrect migrations are where one of the levels in the path is more than 80 chars
            parsed = urlparse(response.url)
            
            if (parsed.hostname == MIGRATION_TEST_DOMAIN) and any(len(x) > 80 for x in parsed.path.split("/")):
                error = "Slug not migrated"

            yield {
                'url': response.url,
                'original_url': response.request.url,
                'contains_table': contains_table,
                'type': 'page',
                'error': error,
                'referer': ''
            }

            for link in self.link_extractor.extract_links(response):
                if "?" not in link.url:
                    yield response.follow(link, callback=self.parse, errback=self.parse_error)
        
        # Handle files
        except scrapy.exceptions.NotSupported:
            error = ""
            if response.url.startswith(CONTENTFUL_BASE_URL):
                error = "Link to Contentful file"
            yield {
                'url': response.url,
                'original_url': response.request.url,
                'contains_table': False,
                'type': "file",
                "error": "",
                'referer': response.request.headers.get('Referer')
            }
    
    def parse_error(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            request = failure.request
            self.logger.error('HttpError on %s', response.url)

            try:
                original_url = response.request.meta['redirect_urls'][0]
            except KeyError:
                original_url = response.url

            _type = ""
            if CONTENTFUL_BASE_URL in response.url:
                _type = "file"

            yield {
                'url': response.url,
                'original_url': original_url,
                # Provide a description for common statuses, otherwise just pass through the status code
                "error": {404: "404: Page not found", 403: "403: Forbidden"}.get(response.status, response.status),
                'referer': request.headers.get('Referer'),
                "type": _type
            }
