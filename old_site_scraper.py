from urllib.parse import urlparse, urljoin
import scrapy

# TARGET_DOMAIN = 'ctfassets.net'
FOLLOW_DOMAIN = 'www.essex.gov.uk'
MIGRATION_TEST_BASE_URL = "https://portal.whitemoss-5a7067b3.uksouth.azurecontainerapps.io"


class AssetSpider(scrapy.Spider):
    name = "assets"
    start_urls = [
        'https://www.essex.gov.uk/legal-services-legal-basis-tables'
    ]
    # custom_settings = {
    #     "DEPTH_LIMIT": 2
    # }

    def parse(self, response):
        contains_table = bool(response.xpath("//table"))

        if  response.url.startswith(MIGRATION_TEST_BASE_URL):
            try:
                original_url = response.request.meta['redirect_urls'][0]
            except KeyError:
                original_url = response.url
            yield {
                'url': original_url,
                'contains_table': contains_table
            }

        else:
            yield {
                'url': response.url,
                'contains_table': contains_table
            }
            # Follow a href to find new pages
            for link in response.xpath('//a/@href').extract():
                # We want to stay within the same site, consider a link to be relative if
                # it has a path but no host or scheme.
                # This excludes URIs like //www.example.com and mailto:example@example.com
                parsed = urlparse(link)
                relative = parsed.path and not parsed.netloc and not parsed.scheme
                # Follow the link if it's relative or if it's absolute within our domain
                if FOLLOW_DOMAIN in link or relative:
                    if '?' in link:
                        # Skip parameterised requests
                        continue
                    yield response.follow(link, callback=self.parse)
        
            if contains_table:
                yield response.follow(urljoin(MIGRATION_TEST_BASE_URL, urlparse(response.url).path))

        
