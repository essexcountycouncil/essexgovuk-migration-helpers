import json
import datetime
from collections import namedtuple, Counter
from pprint import pprint
from shared.helpers import get_latest_file
from shared.constants import MIGRATION_TEST_BASE_URL
import csv

with open(get_latest_file("./output", "contentful-export")) as f:
    root = json.load(f)

Content = namedtuple(
    "Content", ["slug", "title", "notesForEditors"])

all_content = []

for x in root['entries']:
    slug = x['fields'].get("slug")
    title = x['fields'].get("title")
    notes = x['fields'].get("notesForEditors")

    if title:
        title = title['en-GB']

    if slug:
        slug = f"{MIGRATION_TEST_BASE_URL}/{slug['en-GB']}"

    if notes:
        notes = notes['en-GB']
        all_content.append(
            Content(slug=slug, title=title, notesForEditors=notes))

with open("./output/notes.csv", "w") as f:
    w = csv.writer(f)
    w.writerows(all_content)
