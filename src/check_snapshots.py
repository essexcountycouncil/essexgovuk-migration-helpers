import json
from statistics import mean
from collections import Counter

with open(f"output/snapshots.json") as f:
    s = json.load(f)
    versioned_entries = len(s)
    print(f"Total versioned entries in export:\t{len(s)}")
    versioned_ids = s.keys()
    number_of_each = [len(x['items']) for x in s.values()]
    max_versions, avg_version, counter = max(number_of_each), mean(
        number_of_each), Counter(number_of_each)

    print(f"Max number of versions: {max_versions}")
    print(f"Average number of versions: {avg_version}")
    print(sorted(counter.items()))

    hundreders = [x['items'][0]['snapshot']['fields']['title']['en-GB']
                  for x in s.values() if len(x['items']) == 100]
    print(sorted(hundreders))

    hundreder_ids = [key
                     for key, val in s.items() if len(val['items']) == 100]
    print(sorted(hundreder_ids))


with open("output/contentful-export-knkzaf64jx5x-master-2023-07-17T09-42-06.json") as f:
    s = json.load(f)
    print(f"Total entries in Contentful export:\t{len(s['entries'])}")
    # print(s["entries"][123]["sys"])
    drafts = sum(1 for x in s["entries"] if x["sys"].get(
        "publishedVersion") is None)
    print(f"Drafts in Contenful export:\t{drafts}")

    original_ids = {x["sys"]["id"] for x in s["entries"]}

    print(original_ids.difference(versioned_ids))
