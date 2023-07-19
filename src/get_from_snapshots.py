import json
from pprint import pprint
from datetime import datetime as dt

with open(f"output/snapshots.json") as f:
    snapshots = json.load(f)

def get_snapshots_by_entry_id(entry_id: str) -> str:
    for snapshot in snapshots[entry_id]['items']:
        published_at = snapshot['snapshot']['sys']['publishedAt']
        # This will need adjusting 
        body = snapshot['snapshot']['fields']['body']['en-GB']

        published_at = f'⬇ Version published at {dt.fromisoformat(published_at).strftime("%A %d %Y, %H:%M")} ⬇'

        yield published_at, "\n", body


# Example here, replace the entry ID with the one you're looking for
for snapshot in get_snapshots_by_entry_id("4xD7PsTdnfI58CzLH1Atmw"):
    for line in snapshot:
        print(line)
