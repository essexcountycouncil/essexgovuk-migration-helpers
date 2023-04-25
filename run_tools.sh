currentDate=`date +%Y-%m-%d_%H%M`

# pipenv run scrapy runspider src/scraper_old_site.py -o "./output/oldcrawl$currentDate.csv"

# pipenv run python src/redirects_get_contentful.py

# pipenv run python src/redirects_check_wildcards.py

pipenv run scrapy runspider src/scraper_new_site.py -o "./output/newcrawl$currentDate.csv"

# pipenv run scrapy runspider scraper_verify_tables.py -o "./output/tablecrawl$currentDate.csv"