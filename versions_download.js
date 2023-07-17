const contentful = require('contentful-management');
const fs = require('fs');

const client = contentful.createClient({
  accessToken: process.env.CMA_API_KEY,
});

const getData = async () => {
  let allEntries = []
  let entries = {}

  let skip = 0
  let total = 100
  while (skip < total) {
    entries = await client
      .getSpace('knkzaf64jx5x')
      .then((space) => space.getEnvironment('master'))
      .then((env) => env.getEntries({ skip }))
      .catch(console.error);

    allEntries = [...allEntries, ...entries.items]
    skip += entries.items.length
    total = entries.total
  }

  const snapshots = {};

  const calls = allEntries.map(async (item) => {
    return await item
      .getSnapshots()
      .then((data) => {
        snapshots[item.sys.id] = data;
      })
      .catch(console.error);
  });

  await Promise.all(calls);
  console.log('OK', snapshots);

  fs.writeFileSync('output/snapshots.json', JSON.stringify(snapshots), 'utf8', (err) => {
    console.log(err);
    if (err) throw err;
    console.log('complete');
  });
};

getData();