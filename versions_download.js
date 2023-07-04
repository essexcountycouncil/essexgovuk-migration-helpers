const contentful = require('contentful-management');
const fs = require('fs');

const client = contentful.createClient({
  accessToken: process.env.CMA_API_KEY,
});

const getData = async () => {
  const entries = await client
    .getSpace('knkzaf64jx5x')
    .then((space) => space.getEnvironment('master'))
    .then((env) => env.getEntries())
    .catch(console.error);

  const snapshots = {};

  const calls = entries.items.map(async (item) => {
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
