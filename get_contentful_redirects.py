import os
import requests
import json

CDA_API_KEY = os.environ["CDA_API_KEY"]

redirects = requests.get(f"https://cdn.contentful.com/spaces/knkzaf64jx5x/environments/master/entries/638ONr6e4wyaoOo6w8oISU?access_token={CDA_API_KEY}").json()

redirects = redirects['fields']["redirects"] | redirects["fields"]["legacyUrls"]

with open("output/contentful_redirects.json", "w") as f:
    json.dump(redirects, f)
