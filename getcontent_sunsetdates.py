import json
import datetime
from collections import namedtuple, Counter
from pprint import pprint
from shared.helpers import get_latest_file
from shared.constants import MIGRATION_TEST_BASE_URL
import csv

with open(get_latest_file("./output", "contentful-export")) as f:
    root = json.load(f)

Content = namedtuple("Content", ["sunsetDate", "contentType", "slug", "title"])

content_with_sunset_date = []

for x in root['entries']:
    sunset_date = x['fields'].get("sunsetDate")
    content_type = x['sys']['contentType']['sys']['id']
    slug = x['fields'].get("slug")
    title = x['fields'].get("title")

    if title:
        title = title['en-GB']

    if slug:
        slug = slug['en-GB']

    if sunset_date:
        all_content.append(Content(sunsetDate = datetime.datetime.fromisoformat(sunset_date['en-GB']), contentType = content_type, slug=slug, title=title))


content_type_sunset_dates = [x.contentType for x in content_with_sunset_date]

print(f"Total number of items with sunset dates:")
pprint(Counter(content_type_sunset_dates))

content_sunset_before_now = [x for x in all_content if x.sunsetDate < datetime.datetime.now(datetime.timezone.utc)]

print(f"Number of items with sunset dates before now:")
pprint(Counter([x.contentType for x in content_sunset_before_now]))

problem_news_stories = [[x.title, f"{MIGRATION_TEST_BASE_URL}/news/{x.slug}"] for x in content_sunset_before_now]

with open("./output/problem_news_stories.csv", "w") as f:
    w = csv.writer(f)
    w.writerows(problem_news_stories)
    