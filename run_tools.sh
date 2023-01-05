currentDate=`date +%Y-%m-%d_%H%M`
echo ./output/output$currentDate.csv
pipenv run scrapy runspider old_site_scraper.py -o "./output/$currentDate.csv"

# pipenv run python get_contentful_redirects.py

# pipenv run python old_site_scraper_process_data.py
