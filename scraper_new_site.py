from urllib.parse import urlparse, urljoin
import scrapy
import os
import csv
from pprint import pprint

from scraper_base import BaseScraper
from constants import (
    MIGRATION_TEST_DOMAIN,
    MIGRATION_TEST_BASE_URL,
    MIGRATION_TEST_MOCK_URL,
    CONTENTFUL_DOMAIN,
    OLD_BASE_URL,
)


def process_from_url(row):
    """Extract a clean url path from Contentful redirects"""
    url = row["from_url"]
    url = url.replace(" ", "%20")
    url = urlparse(url).path
    url = url.replace("*", "Vyx2gbebyyyV6bA5")
    return url


def get_urls():
    """
    Get all the URLs we need, includes:
    * Redirects from Contentful export
    * Results from the crawl of the old site

    Add the new site domain to the paths
    """

    # Get all the redirect URLs from the Contentful export
    with open("./output/contentful_redirects.csv") as f:
        reader = csv.DictReader(f)
        redirect_from_urls = [process_from_url(row) for row in reader]

    # Find the latest old crawl file in the directory and open it
    oldcrawl_latest = sorted(
        [x for x in os.listdir("./output") if x.startswith("oldcrawl")]
    )[-1]

    with open(os.path.join("./output", oldcrawl_latest)) as f:
        old_urls = [x["url"] for x in csv.DictReader(f)]

    # We're only bringing in essex.gov.uk URLs from the old crawl
    # i.e. we're excluding any ctfassets url
    old_urls = [urlparse(x).path for x in old_urls if x.startswith(OLD_BASE_URL)]

    # Add in specific URLs here that we need to check (linked from Achieve form) that won't be picked up by the crawl
    all_urls = redirect_from_urls + old_urls + ["care-calculator-complete-eligible", "care-calculator-self-funded"]

    all_urls = [urljoin(MIGRATION_TEST_BASE_URL, x) for x in all_urls]

    return all_urls


class NewSiteScraper(BaseScraper):
    """
    New site scraper

    * Gets the start URLs from redirects, crawl, and mock home page
    * Scrape everything
    """

    name = "newsite"

    start_urls = [MIGRATION_TEST_BASE_URL, MIGRATION_TEST_MOCK_URL] + get_urls()
    allowed_domains = [MIGRATION_TEST_DOMAIN, CONTENTFUL_DOMAIN]

    # deny_extensions = [] means that we don't exclude files from being checked
    link_extractor = scrapy.linkextractors.LinkExtractor(
        allow_domains=allowed_domains, deny_extensions=[]
    )

    # Uncomment this if you want to restrict the depth limit - can be handy for testing
    # custom_settings = {
    #     "DEPTH_LIMIT": 1
    # }
