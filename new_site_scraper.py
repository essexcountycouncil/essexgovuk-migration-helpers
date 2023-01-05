from urllib.parse import urlparse, urljoin
import scrapy

from basescraper import BaseScraper
from constants import MIGRATION_TEST_DOMAIN, MIGRATION_TEST_BASE_URL, MIGRATION_TEST_MOCK_URL, CONTENTFUL_DOMAIN

class NewSiteScraper(BaseScraper):
    name = "newsite"
    start_urls = [MIGRATION_TEST_BASE_URL, MIGRATION_TEST_MOCK_URL]
    allowed_domains = [MIGRATION_TEST_DOMAIN, CONTENTFUL_DOMAIN]
    
    link_extractor = scrapy.linkextractors.LinkExtractor(allow_domains=allowed_domains, deny_extensions=[])

    # Uncomment this if you want to restrict the depth limit - can be handy for testing
    # custom_settings = {
    #     "DEPTH_LIMIT": 1
    # }
