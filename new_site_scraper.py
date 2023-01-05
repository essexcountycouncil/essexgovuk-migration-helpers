from urllib.parse import urlparse, urljoin
import scrapy
import os
import csv
import json

from basescraper import BaseScraper
from constants import MIGRATION_TEST_DOMAIN, MIGRATION_TEST_BASE_URL, MIGRATION_TEST_MOCK_URL, CONTENTFUL_DOMAIN

class NewSiteScraper(BaseScraper):
    name = "newsite"
    # TODO make start_urls read from the files
    start_urls = [MIGRATION_TEST_BASE_URL, MIGRATION_TEST_MOCK_URL]
    allowed_domains = [MIGRATION_TEST_DOMAIN, CONTENTFUL_DOMAIN]
    
    link_extractor = scrapy.linkextractors.LinkExtractor(allow_domains=allowed_domains, deny_extensions=[])

    # Uncomment this if you want to restrict the depth limit - can be handy for testing
    # custom_settings = {
    #     "DEPTH_LIMIT": 1
    # }


def get_urls():
    with open("./output/contentful_redirects.json") as f:
        redirects = json.load(f)

    redirects = [x for x, _ in redirects.items()]

    
    oldcrawl_latest = [x for x in os.listdir("./output") if x.startswith("oldcrawl")][-1]

    with open(os.path.join("./output", oldcrawl_latest)) as f:
        old_urls = [x['url'] for x in csv.DictReader(f)]
    
    # TODO add in the base URLs to the start or replace the old base URL for the new one as required

    all_urls = redirects + old_urls

    print(all_urls)

get_urls() 


