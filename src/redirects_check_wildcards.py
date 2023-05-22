import csv
import requests

with open("output/contentful_redirects.csv") as f:
    redirects = csv.DictReader(f)

    wildcards = [
        (r["from_url"].rstrip("*"),
         r["to_url"].replace("https://www.essex.gov.uk/", ""))
        for r in redirects
        if r["from_url"].endswith("*")
    ]


should_be_rewrites = {
    f"rewrite '^({key}.*)$' https://$customhost/{value} permanent;"
    for key, value in wildcards
}

nginx = requests.get(
    "https://raw.githubusercontent.com/essexcountycouncil/essex-gov-uk-drupal/develop/nginx-conf/nginx.conf"
).text

nginx = [line.lstrip() for line in nginx.split("\n")]
rewrites = {line for line in nginx if line.startswith("rewrite")}


output = "The following lines need to be added to https://github.com/essexcountycouncil/essex-gov-uk-drupal/blob/develop/nginx-conf/nginx.conf\n\n"

for rewrite in should_be_rewrites.difference(rewrites):
    output += rewrite
    output += "\n"

with open("./output/redirects_missing_wildcard.txt", "w+") as f:
    f.write(output)
