import json
import datetime
from collections import namedtuple, Counter
from pprint import pprint
from shared.helpers import get_latest_file
from shared.constants import MIGRATION_TEST_BASE_URL, OLD_BASE_URL
import csv
import os
from functools import reduce

with open(get_latest_file("./output", "contentful-export")) as f:
    root = json.load(f)

Content = namedtuple(
    "Content", ["contentfulID", "contentType", "slug", "title", "sections"]
)


def fetch_data():
    all_content = {}
    for x in root["entries"]:
        contentful_id = x["sys"]["id"]
        content_type = x["sys"]["contentType"]["sys"]["id"]
        slug = x["fields"].get("slug")
        title = x["fields"].get("title")
        sections = x["fields"].get("sections")

        if title:
            title = title["en-GB"]

        if slug:
            slug = slug["en-GB"]

        if sections:
            sections = [x["sys"]["id"] for x in sections["en-GB"]]

        all_content[contentful_id] = Content(
            contentfulID=contentful_id,
            contentType=content_type,
            slug=slug,
            title=title,
            sections=sections,
        )

    return all_content


all_content = fetch_data()

info_pages = []

all_list = []
with open("./output/fathom_data.json") as f:
    fathom_data = json.load(f)
    for sublist in fathom_data:
        all_list.extend(sublist)

for _, info_page in all_content.items():
    output = {}
    if not ((info_page.contentType == "article") and info_page.sections):
        continue

    output["overview_title"] = info_page.title
    output["url"] = f"{OLD_BASE_URL}/{info_page.slug}"
    page_titles = []
    for section in info_page.sections:
        section = all_content.get(section)
        if section:
            page_titles.append(section.title)

    output["page_titles"] = page_titles

    output["page_views"] = sum(
        int(d["views"]) for d in all_list if d["label"].startswith(f"/{info_page.slug}")
    )

    info_pages.append(output)

with open(os.path.join("./output", "overviews.json"), "w") as f:
    json.dump(info_pages, f)

with open(os.path.join("./output", "overviews.csv"), "w") as f:
    w = csv.writer(f)
    w.writerow(["Total views", "url", "Guide title", "First section title"])
    for page in info_pages:
        w.writerow(
            [
                page["page_views"],
                page["url"],
                page["overview_title"],
                *page["page_titles"],
            ]
        )
