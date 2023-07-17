const contentful = require('contentful-management');
const fs = require('fs');
const entries = JSON.parse(fs.readFileSync('output/contentful_entry_ids.json', 'utf-8'))

const first_two_hundred = entries.slice(0, 1)

const client = contentful.createClient({
  accessToken: process.env.CMA_API_KEY,
  rateLimit: 1
});

const snapshots = {};

const getEntry = async (entryID) => {
  client.getSpace('knkzaf64jx5x')
    .then((space) => space.getEnvironment('master'))
    .then((environment) => environment.getEntrySnapshots(entryID))
    .then((data) => {
      console.log(data);
      snapshots[entryID] = data;
    })
    .catch(console.error)
}

const getData = async () => {
  const calls = first_two_hundred.map(async (entryID) => {
    return await getEntry(entryID)
      .then((data) => {
        snapshots[entryID] = data;
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