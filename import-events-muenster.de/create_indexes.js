
const request = require('request-promise-native')

const elasticsearchUrlPrefix = "https://api.muenster.jetzt/"
const indices = {}

indices.infohub = {
  mappings: {
      properties: {
        start_date: {
          type:"date"
        },
        date_end: {
          type:"date"
        },
        geo: {
          type: 'geo_point',
        },
        geometry: {
          type: 'geo_shape',
        },
      },
  },
}



console.log('Deleting and recreating indices with mapping..')

for (const [indexName, mapping] of Object.entries(indices)) {
  const indexUrl = `${elasticsearchUrlPrefix}${indexName}`


  console.log('Deleting index ' + indexUrl)
  request.delete({
    url: `${indexUrl}`,
    json: true,
  })
    .then((response) => {
      // console.log(`Success: ${indexUrl}`);
      // console.log(response);
    })
    .catch((err) => {
      console.log(`Error deleting: ${indexUrl}`)
      console.log(err.message)
    })

    console.log('Creating index with mapping: ' + indexUrl)
    request.put({
    url: `${indexUrl}`,
    json: true,
    body: mapping,
  })
    .then((response) => {
      console.log(`Success creating: ${indexUrl}`)
      // console.log(response);
    })
    .catch((err) => {
      console.log(`Error creating: ${indexUrl}`)
      console.log(err.message)
    })
}
