import os
import requests

CDA_API_KEY = os.environ["CDA_API_KEY"]

redirects = requests.get(f"https://cdn.contentful.com/spaces/knkzaf64jx5x/environments/master/entries/638ONr6e4wyaoOo6w8oISU?access_token={CDA_API_KEY}").json()

print(redirects)