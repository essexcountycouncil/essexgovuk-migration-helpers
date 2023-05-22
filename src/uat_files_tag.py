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
t/e.txt""".split()

for fn in filenames:
    r = requests.get(f"https://beta.essex.gov.uk/{fn}")
    tag = r.headers["x-robots-tag"]
    print(tag)
    assert tag == "noindex"
    break

filenames_bad = """foo.js
crea/bar.js
test/hello.css
whatever
something-diffe/rent""".split()


for fn in filenames_bad:
    r = requests.get(f"https://beta.essex.gov.uk/{fn}")
    try:
        tag = r.headers["x-robots-tag"]
    except Exception as e:
        assert isinstance(e, KeyError)
    print(tag)
