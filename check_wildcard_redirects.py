import json
import requests

with open("output/contentful_redirects.json") as f:
    redirects = json.load(f)

wildcards = [(key.rstrip("*"), value.replace("https://www.essex.gov.uk/", "")) for (key, value) in redirects.items() if key.endswith("*")]
    

should_be_rewrites = {f"rewrite '^({key}.*)$' https://$host/{value} permanent;" for key, value in wildcards}

nginx = requests.get("https://raw.githubusercontent.com/essexcountycouncil/essex-gov-uk-drupal/develop/nginx-conf/nginx.conf").text

nginx = [line.lstrip() for line in nginx.split("\n")]
rewrites = {line for line in nginx if line.startswith("rewrite")}


output = "The following lines need to be added to https://github.com/essexcountycouncil/essex-gov-uk-drupal/blob/develop/nginx-conf/nginx.conf\n\n"

for rewrite in should_be_rewrites.difference(rewrites):
    output += rewrite
    output += "\n"

with open("output/missing_wildcard_redirects.txt", "w+") as f:
    f.write(output)
