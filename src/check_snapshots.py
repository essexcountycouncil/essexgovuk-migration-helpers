import json

for version in range(1, 6):

    with open(f"output/snapshots_20230717v{version}.json") as f:
        s = json.load(f)
        print(f"Total versioned entries in export v{version}:\t{len(s)}")
        versioned_ids = s.keys()


with open("output/contentful-export-knkzaf64jx5x-master-2023-07-17T09-42-06.json") as f:
    s = json.load(f)
    print(f"Total entries in Contentful export:\t{len(s['entries'])}")
    # print(s["entries"][123]["sys"])
    drafts = sum(1 for x in s["entries"] if x["sys"].get(
        "publishedVersion") is None)
    print(f"Drafts in Contenful export:\t{drafts}")

    original_ids = [x["sys"]["id"] for x in s["entries"]]

with open("output/contentful_entry_ids.json", "w") as f:
    json.dump(original_ids, f)


# print(original_ids.difference(versioned_ids))
