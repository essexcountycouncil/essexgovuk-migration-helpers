import json
import datetime
from collections import namedtuple, Counter
from pprint import pprint
from shared.helpers import get_latest_file
from shared.constants import MIGRATION_TEST_BASE_URL
import csv

with open(get_latest_file("./output", "contentful-export")) as f:
    root = json.load(f)

Content = namedtuple("Content", ["contentType", "slug", "title", "first_section_id"])

all_content = {}

for x in root["entries"]:
    id = x["sys"]["id"]
    sunset_date = x["fields"].get("sunsetDate")
    content_type = x["sys"]["contentType"]["sys"]["id"]
    slug = x["fields"].get("slug")
    title = x["fields"].get("title")
    sections = x["fields"].get("sections")

    if title:
        title = title["en-GB"]

    if slug:
        slug = slug["en-GB"]

    if sections:
        first_section_id = sections["en-GB"][0]["sys"]["id"]
        # print(first_section_id)
    else:
        first_section_id = None

    all_content[id] = Content(
        contentType=content_type,
        slug=slug,
        title=title,
        first_section_id=first_section_id,
    )

info_pages = [
    x
    for _, x in all_content.items()
    if ((x.contentType == "article") and x.first_section_id)
]

info_pages_first_titles = [
    (page.title, all_content[page.first_section_id].title) for page in info_pages
]

# pprint(info_pages_first_titles)

overviews = [x for x in info_pages_first_titles if "overview" in x[1].lower()]

print(f"Overviews: total {len(overviews)}")
pprint(overviews)

not_overviews = [x for x in info_pages_first_titles if "overview" not in x[1].lower()]

print(f"Not Overviews: total {len(not_overviews)}")
pprint(not_overviews)

# content_type_sunset_dates = [x.contentType for x in content_with_sunset_date]

# print(f"Total number of items with sunset dates:")
# pprint(Counter(content_type_sunset_dates))

# content_sunset_before_now = [x for x in all_content if x.sunsetDate < datetime.datetime.now(datetime.timezone.utc)]

# print(f"Number of items with sunset dates before now:")
# pprint(Counter([x.contentType for x in content_sunset_before_now]))

# problem_news_stories = [[x.title, f"{MIGRATION_TEST_BASE_URL}/news/{x.slug}"] for x in content_sunset_before_now]

# with open("./output/problem_news_stories.csv", "w") as f:
#     w = csv.writer(f)
#     w.writerows(problem_news_stories)
