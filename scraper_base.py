import scrapy
from urllib.parse import urlparse

from constants import CONTENTFUL_BASE_URL, MIGRATION_TEST_DOMAIN


class BaseScraper(scrapy.Spider):
    result_fields = (
        "url",
        "original_url",
        "title",
        "contains_table",
        "type",
        "error",
        "referer",
    )

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

        result = {x: "" for x in self.result_fields}
        result["url"] = response.url
        result["original_url"] = response.request.url
        result["referer"] = response.request.headers.get("Referer")

        try:
            result["contains_table"] = bool(response.xpath("//table"))
            result["title"] = response.xpath("//title/text()").get()
            result["type"] = "page"

            all_text = "".join(x.get() for x in response.xpath("//text()"))

            # Flag urls where the slug has not migrated correctly
            # Incorrect migrations are where one of the levels in the path is more than 80 chars
            parsed = urlparse(response.url)

            if parsed.hostname == MIGRATION_TEST_DOMAIN:
                if inline_error := "{{Alerts-Inline" in all_text:
                    result["error"] = "Incorrect inline alert"
                    yield result

                if slug_error := any(
                    len(x) > 50 for x in parsed.path.replace("-", "/").split("/")
                ):
                    result["error"] = "Slug not migrated"
                    yield result

                if not inline_error or slug_error:
                    yield result

            else:
                yield result

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
            result["type"] = "file"

            # Flag links to Contentful files
            if response.url.startswith(CONTENTFUL_BASE_URL):
                result["error"] = "Link to Contentful file"

            yield result

    def parse_error(self, failure):
        """
        Handles HTTP errors
        * Notes original URL for redirects
        * Marks files where possible
        * Yield result for scrapy to output
        """

        result = {x: "" for x in self.result_fields}

        request = failure.request

        # Find the original URL when we're doing redirects
        try:
            result["original_url"] = request.meta["redirect_urls"][0]
        except KeyError:
            result["original_url"] = request.url

        # If it's a HttpError we can provide quite a lot of information
        if failure.check(scrapy.spidermiddlewares.httperror.HttpError):
            response = failure.value.response
            result["url"] = response.url

            # Flag files where possible.
            # This includes both Contentful and migrated files
            # (because the migrated ones still have assets.ctfassets.net in them)
            if CONTENTFUL_BASE_URL in response.url:
                result["type"] = "file"

            result["error"] = {404: "404: Page not found", 403: "403: Forbidden"}.get(
                response.status, response.status
            )
            result["referer"] = request.headers.get("Referer")

        # Otherwise, we have fairly limited information (we expect DNS errors here)
        else:
            result["url"] = request.url
            result["error"] = failure.getErrorMessage()

        yield result
