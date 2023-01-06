currentDate=`date +%Y-%m-%d_%H%M`

# pipenv run scrapy runspider old_site_scraper.py -o "./output/oldcrawl$currentDate.csv"

# pipenv run python get_contentful_redirects.py

# pipenv run python old_site_scraper_process_data.py

pipenv run scrapy runspider scraper_new_site.py -o "./output/newcrawl$currentDate.csv"
