import csv
import os
from urllib.parse import urlparse, urljoin
import scrapy

from scraper_base import BaseScraper
from constants import OLD_BASE_URL, MIGRATION_TEST_BASE_URL, MIGRATION_TEST_DOMAIN

# Find the latest old crawl file in the directory
oldcrawl_latest = sorted(
    [x for x in os.listdir("./output") if x.startswith("oldcrawl")]
)[-1]

with open(os.path.join("./output", oldcrawl_latest)) as f:
    # Slightly awkward way we have to check this - disadvantage of using csvs!
    old_urls = [x["url"] for x in csv.DictReader(f) if x["contains_table"] == "True"]
    old_urls = [urlparse(x).path for x in old_urls if x.startswith(OLD_BASE_URL)]
    old_urls = [urljoin(MIGRATION_TEST_BASE_URL, x) for x in old_urls]


class VerifyTablesScraper(BaseScraper):
    """
    Check that tables appear correctly
    """
    
    name = "verifytables"

    start_urls = old_urls
    allowed_domains = [MIGRATION_TEST_DOMAIN]

    link_extractor = scrapy.linkextractors.LinkExtractor(allow_domains=allowed_domains)

    def parse(self, response):
        contains_table = bool(response.xpath("//table"))

        if not contains_table:
            yield {"url": response.url, "error": "Table error"}
