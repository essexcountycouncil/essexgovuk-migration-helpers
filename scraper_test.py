from scraper_base import BaseScraper
from constants import (
    MIGRATION_TEST_DOMAIN,
    CONTENTFUL_DOMAIN,
)
import scrapy


class NewSiteScraper(BaseScraper):
    """
    New site scraper

    * Gets the start URLs from redirects, crawl, and mock home page
    * Scrape everything
    """

    name = "newsite"

    start_urls = ["https://www-essex-gov-uk.nomensa.xyz/Publications/asdsadsa"]
    allowed_domains = [MIGRATION_TEST_DOMAIN, CONTENTFUL_DOMAIN]

    # deny_extensions = [] means that we don't exclude files from being checked
    link_extractor = scrapy.linkextractors.LinkExtractor(
        allow_domains=allowed_domains, deny_extensions=[]
    )

    custom_settings = {"DEPTH_LIMIT": 1}
