# essex.gov.uk migration helpers

This is a one-off project to spider essex.gov.uk and find all files hosted on the contentful asset CDN that are in use, to aid in migration.

## Running

N.B.: These files are appended to, so if you'd like to re-run the spider then delete these files if present.

### Python

Ensure you have Python 3.9 installed, as well as pipenv. Then run the following:

    pipenv install
    pipenv run scrapy runspider old_site_scraper.py -o ./output/output.csv
