import scrapy
from urllib.parse import urlparse

from constants import CONTENTFUL_BASE_URL, MIGRATION_TEST_DOMAIN


class BaseScraper(scrapy.Spider):
    def start_requests(self):
        """Override scrapy's defaults to call parse_error for start_urls that error"""
        for u in self.start_urls:
            yield scrapy.Request(u, errback=self.parse_error)

    def parse(self, response):
        """
        Parsing function to handle all responses.
        * Checks if there's a table
        * Checks if there's a slug migration error
        * For pages follow all links
        * Yield result for scrapy to output
        """
        try:
            contains_table = bool(response.xpath("//table"))

            # Flag urls where the slug has not migrated correctly
            # Incorrect migrations are where one of the levels in the path is more than 80 chars
            error = ""
            parsed = urlparse(response.url)
            if (parsed.hostname == MIGRATION_TEST_DOMAIN) and any(
                len(x) > 80 for x in parsed.path.split("/")
            ):
                error = "Slug not migrated"

            # Yield data
            yield {
                "url": response.url,
                "original_url": response.request.url,
                "contains_table": contains_table,
                "type": "page",
                "error": error,
                "referer": "",
            }

            # Follow links in page
            for link in self.link_extractor.extract_links(response):
                # Exclude links with parameters - otherwise you end up repeating the same pages
                if "?" not in link.url:
                    # Must include errback param here so that errors are also logged
                    yield response.follow(
                        link, callback=self.parse, errback=self.parse_error
                    )

        # Handle files - files will return NotSupported once xpath is called on them
        except scrapy.exceptions.NotSupported:

            # Flag links to Contentful files
            error = ""
            if response.url.startswith(CONTENTFUL_BASE_URL):
                error = "Link to Contentful file"

            yield {
                "url": response.url,
                "original_url": response.request.url,
                "contains_table": False,
                "type": "file",
                "error": error,
                "referer": response.request.headers.get("Referer"),
            }

    def parse_error(self, failure):
        """
        Handles HTTP errors
        * Notes original URL for redirects
        * Marks files where possible
        * Yield result for scrapy to output
        """

        ### Filter out other kinds of errors, we just want HttpError
        if not failure.check(scrapy.spidermiddlewares.httperror.HttpError):
            return

        response = failure.value.response
        request = failure.request

        # Find the original URL when we're doing redirects
        try:
            original_url = request.meta["redirect_urls"][0]
        except KeyError:
            original_url = response.url

        # Flag files where possible.
        # This includes both Contentful and migrated files
        # (because the migrated ones still have assets.ctfassets.net in them)
        _type = ""
        if CONTENTFUL_BASE_URL in response.url:
            _type = "file"

        yield {
            "url": response.url,
            "original_url": original_url,
            # Provide a description for common statuses, otherwise just pass through the status code
            "error": {404: "404: Page not found", 403: "403: Forbidden"}.get(
                response.status, response.status
            ),
            "referer": request.headers.get("Referer"),
            "type": _type,
        }
