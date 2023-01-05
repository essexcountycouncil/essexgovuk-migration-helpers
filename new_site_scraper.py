from urllib.parse import urlparse, urljoin
import scrapy

from basescraper import BaseScraper
from constants import OLD_DOMAIN, OLD_BASE_URL, CONTENTFUL_DOMAIN

class OldSiteScraper(BaseScraper):
    name = "oldsite"
    start_urls = [OLD_BASE_URL]
    allowed_domains = [OLD_DOMAIN, CONTENTFUL_DOMAIN]
    
    link_extractor = scrapy.linkextractors.LinkExtractor(allow_domains=allowed_domains, deny_extensions=[])

    # Uncomment this if you want to restrict the depth limit - can be handy for testing
    # custom_settings = {
    #     "DEPTH_LIMIT": 1
    # }
