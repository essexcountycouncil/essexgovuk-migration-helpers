import requests
from itertools import count
import json

has_more_pages = True

all_numbers = []


def save():
    with open("./output/fathom_data.json", "w") as f:
        json.dump(all_numbers, f)


for page in count():
    try:
        data = requests.get(
            f"https://app.usefathom.com/sites/HVSTNHSN/boxes/pages?page={page}&range=all_time&sort=visitors%3Adesc&tz=Europe/London"
        ).json()
        all_numbers.append(data["rows"])
        if not data["has_more_pages"]:
            break
    except:
        save()

        raise Exception(f"I got to page {page-1}")

save()
