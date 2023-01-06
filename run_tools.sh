currentDate=`date +%Y-%m-%d_%H%M`

# pipenv run scrapy runspider scraper_old_site.py -o "./output/oldcrawl$currentDate.csv"

# pipenv run python redirects_get_contentful.py

# pipenv run python redirects_check_wildcards.py

# pipenv run scrapy runspider scraper_new_site.py -o "./output/newcrawl$currentDate.csv"

pipenv run scrapy runspider scraper_verify_tables.py -o "./output/tablecrawl$currentDate.csv"