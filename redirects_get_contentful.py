import os
import requests
import csv

# You need to set CDA_API_KEY as an environment variable
CDA_API_KEY = os.environ["CDA_API_KEY"]

redirects = requests.get(
    f"https://cdn.contentful.com/spaces/knkzaf64jx5x/environments/master/entries/638ONr6e4wyaoOo6w8oISU?access_token={CDA_API_KEY}"
).json()

redirects = redirects["fields"]["redirects"] | redirects["fields"]["legacyUrls"]

with open("./output/contentful_redirects.csv", "w+") as f:
    writer = csv.writer(f)
    writer.writerow(["from_url", "to_url"])
    for from_url, to_url in redirects.items():
        writer.writerow([from_url, to_url])
