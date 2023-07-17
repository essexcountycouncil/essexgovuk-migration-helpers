import contentful_management
import os
import json

SPACE_ID = "knkzaf64jx5x"
CMA_API_KEY = os.environ['CMA_API_KEY']

client = contentful_management.Client(CMA_API_KEY)
environment = client.environments(SPACE_ID).find('master')

snapshots = dict()


def read_entry_ids() -> list[str]:

    with open("output/contentful_entry_ids.json") as f:
        entry_ids = json.load(f)

    return entry_ids


def get_versions_by_entry_id(entry_id: str) -> list:
    print(f"Requesting entry {entry_id}...")
    eeee = [x.to_json()
            for x in environment.entries().find(entry_id).snapshots().all()]
    print(eeee)


def save_to_file() -> None:
    with open("output/snapshots_python.json", "w") as f:
        json.dump(snapshots, f)


entry_ids = read_entry_ids()

for entry_id in entry_ids:
    try:
        snapshots[entry_id] = get_versions_by_entry_id(
            "4I5peHWWwUWOyoyCAcs4C2")
        break
    except KeyboardInterrupt:
        save_to_file()

save_to_file()
