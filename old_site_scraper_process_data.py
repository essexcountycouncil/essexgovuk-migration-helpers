import csv
from urllib.parse import urlparse, urljoin

OLD_BASE = "https://www.essex.gov.uk"
NEW_BASE = "https://portal.whitemoss-5a7067b3.uksouth.azurecontainerapps.io"

paths = set()
results_all = dict()
results_combined = []

with open("output.csv") as f:
    rows = csv.reader(f)
    for row in rows:
        if row[0] == "url":
            continue
        paths.add(urlparse(row[0]).path)
        results_all[row[0]] = row[1]
    
for path in paths: 
    old_path = urljoin(OLD_BASE, path)
    new_path = urljoin(NEW_BASE, path)
    
    try:
        old_has_table = results_all[old_path]
    except KeyError:
        old_has_table = ""
        
    try:
        new_has_table = results_all[new_path]
    except KeyError:
        new_has_table = ""

    results_combined.append({"old_path": old_path,
    "old_has_table": old_has_table,
    "new_path": new_path,
    "new_has_table": new_has_table})

fieldnames = ["old_path", "old_has_table", "new_path", "new_has_table"]

with open("output/final_output.csv", "w") as f:
    dw = csv.DictWriter(f, fieldnames=fieldnames)
    dw.writeheader()
    dw.writerows(results_combined)
    


