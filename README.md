# essex.gov.uk migration helpers

A suite of tools for detecting errors with automated migration of essex.gov.uk.

## Collecting the content archive from Contentful
These instructions run a script provided by Contentful.
### Dependencies
- Node

### How to run
```bash
npm install -g
node versions_download.js
```

### Looking at the information in the archive
There's an example Python script for accessing information from the snapshots file at [/src/get_from_snapshots.py](https://github.com/essexcountycouncil/essexgovuk-migration-helpers/blob/main/src/get_from_snapshots.py).

You'll need to adjust this script depending on what information you want to retrieve.
