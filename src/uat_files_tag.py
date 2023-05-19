import requests

filenames = """foo.xls
bar.xlsx
bz.xlsm
c.doc
d.docx
e.docm
e.ppt
e.pptx
e.pptm
e.pps
e.ppsx
e.ppsm
t/""".split()

for fn in filenames:
    r = requests.get(f"https://preprod.essex-gov.nomensa.xyz/{fn}")
    tag = r.headers["x-robots-tag"]
    print(tag)
    assert tag == "noindex"
