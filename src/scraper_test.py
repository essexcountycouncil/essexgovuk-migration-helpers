from shared.scraper_base import BaseScraper
from shared.constants import (
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

    start_urls = [
        f"https://www-essex-gov-uk.nomensa.xyz/adult-social-care-and-health/personal-budgets/help-find-your-own-care-and-support"
    ]

    allowed_domains = [MIGRATION_TEST_DOMAIN, CONTENTFUL_DOMAIN]

    # deny_extensions = [] means that we don't exclude files from being checked
    link_extractor = scrapy.linkextractors.LinkExtractor(
        allow_domains=allowed_domains, deny_extensions=[]
    )

    custom_settings = {"DEPTH_LIMIT": 2}
