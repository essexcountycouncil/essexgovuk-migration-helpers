import json

with open("output/snapshots.json") as f:
    snapshots = json.load(f)

with open("output/snapshots_formatted.json", "w") as f:
    json.dump(snapshots, f, indent=4)
