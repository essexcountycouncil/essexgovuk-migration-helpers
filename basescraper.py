import scrapy

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
                yield response.follow(link, callback=self.parse)
        
        # Handle files
        except scrapy.exceptions.NotSupported:
            yield {
                'url': response.url,
                'status': response.status,
                'type': "file"
            }
