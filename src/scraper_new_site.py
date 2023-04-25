from urllib.parse import urlparse, urljoin
import scrapy
import os
import csv
from pprint import pprint

from shared.scraper_base import BaseScraper
from shared.constants import (
    MIGRATION_TEST_DOMAIN,
    MIGRATION_TEST_BASE_URL,
    MIGRATION_TEST_START_URL,
    CONTENTFUL_DOMAIN,
    OLD_BASE_URL,
)


def process_from_url(row):
    """Extract a clean url path from Contentful redirects"""
    url = row["from_url"]
    url = url.replace(" ", "%20")
    url = urlparse(url).path

    # Use an arbitrary string for wildcard redirects
    url = url.replace("*", "Vyx2gbebyyyV6bA5")

    return url


def get_urls():
    """
    Get all the URLs we need, includes:
    * Redirects from Contentful export
    * Results from the crawl of the old site

    Add the new site domain to the paths
    """

    # Find the latest old crawl file in the directory and open it
    oldcrawl_latest = sorted(
        [x for x in os.listdir("./output") if x.startswith("oldcrawl")]
    )[-1]

    with open(os.path.join("./output", oldcrawl_latest)) as f:
        old_urls = [x["url"] for x in csv.DictReader(f)]

    # We're only bringing in essex.gov.uk URLs from the old crawl
    # i.e. we're excluding any ctfassets url
    old_urls = [
        urlparse(x).path for x in old_urls if x.startswith(OLD_BASE_URL)]

    # SPECIFIC URLs that we need to add
    # not included in the crawl...

    # Contentful redirects
    with open("./output/contentful_redirects.csv") as f:
        redirect_from_urls = [process_from_url(
            row) for row in csv.DictReader(f)]

    # Linked from Achieve form
    achieve_urls = ["care-calculator-complete-eligible",
                    "care-calculator-self-funded"]

    # News URLs - going through each page in the pagination
    news_urls = [f"news?page={i}" for i in range(1, 80)]

    all_urls = redirect_from_urls + old_urls + achieve_urls + news_urls

    # Add in the base URL
    all_urls = [urljoin(MIGRATION_TEST_BASE_URL, x) for x in all_urls]

    return all_urls


class NewSiteScraper(BaseScraper):
    """
    New site scraper

    * Gets the start URLs from redirects, crawl, and mock home page
    * Scrape everything
    """

    name = "newsite"

    start_urls = [MIGRATION_TEST_BASE_URL,
                  MIGRATION_TEST_START_URL,] + get_urls()
    allowed_domains = [MIGRATION_TEST_DOMAIN, CONTENTFUL_DOMAIN]

    # deny_extensions = [] means that we don't exclude files from being checked
    link_extractor = scrapy.linkextractors.LinkExtractor(
        allow_domains=allowed_domains, deny_extensions=[]
    )
