currentDate=`date +%Y-%m-%d_%H%M`

# pipenv run scrapy runspider old_site_scraper.py -o "./output/oldcrawl$currentDate.csv"

# pipenv run python get_contentful_redirects.py

# pipenv run python old_site_scraper_process_data.py

pipenv run scrapy runspider new_site_scraper.py -o "./output/newcrawl$currentDate.csv"

# pipenv run scrapy runspider new_site_verifier.py -o "./output/newverify$currentDate.csv"