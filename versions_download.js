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

      .catch(console.error)



    allEntries = [...allEntries, ...entries.items]

    skip += entries.items.length

    total = entries.total

  }

  const totalLenEntries = allEntries.length

  console.log('Total Entries count', totalLenEntries)



  const snapshots = {}

  for (let index = 0; index < totalLenEntries; index++) {

    console.log('Getting Snapshots Progress: %d%', (((index + 1) / totalLenEntries) * 100).toFixed(2))

    const entry = allEntries[index]

    await entry

      .getSnapshots()

      .then((data) => {

        snapshots[entry.sys.id] = data;

      })

      .catch(console.error);

  }



  console.log('Total snapshots for entries', Object.keys(snapshots).length)



  fs.writeFileSync('output/snapshots.json', JSON.stringify(snapshots), 'utf8', (err) => {

    console.log(err)

    if (err) throw err

    console.log('complete')

  })

}



getData()
