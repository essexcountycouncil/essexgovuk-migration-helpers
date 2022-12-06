from urllib.parse import urlparse, urljoin
import scrapy

from constants import OLD_DOMAIN, OLD_BASE_URL, MIGRATION_TEST_BASE_URL

class OldSiteScraper(scrapy.Spider):
    name = "oldsite"
    start_urls = [OLD_BASE_URL]

    # Uncomment this if you want to restrict the depth limit - can be handy for testing
    custom_settings = {
        "DEPTH_LIMIT": 1
    }

    def parse(self, response):

        contains_table = bool(response.xpath("//table"))

        if response.url.startswith(MIGRATION_TEST_BASE_URL):
            try:
                original_url = response.request.meta['redirect_urls'][0]
            except KeyError:
                original_url = response.url
            yield {
                'url': original_url,
                'contains_table': contains_table,
                'status': response.status
            }

        else:
            yield {
                'url': response.url,
                'contains_table': contains_table,
                'status': response.status
            }

            # Follow a href to find new pages
            for link in response.xpath('//a/@href').extract():

                # We want to stay within the same site, consider a link to be relative if
                # it has a path but no host or scheme.
                # This excludes URIs like //www.example.com and mailto:example@example.com
                parsed = urlparse(link)
                relative = parsed.path and not parsed.netloc and not parsed.scheme

                # Follow the link if it's relative or if it's absolute within our domain
                if OLD_DOMAIN in link or relative:
                    
                    # Skip parameterised requests
                    if '?' in link:
                        continue

                    yield response.follow(link, callback=self.parse)
        
            if contains_table:
                yield response.follow(urljoin(MIGRATION_TEST_BASE_URL, urlparse(response.url).path))
