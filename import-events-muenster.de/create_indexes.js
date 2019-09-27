
const request = require('request-promise-native')

const elasticsearchUrlPrefix = "https://data.mein-ms.de/"
const indices = {}

indices.infohub = {
  mappings: {
    _doc: {
      properties: {
        start_date: {
          type:"date",
          format:"YYYY-MM-DD'T'HH:mm:ssZ"
        },
        date_end: {
          type:"date",
          format:"YYYY-MM-DD'T'HH:mm:ssZ"
        },
        geo: {
          type: 'geo_point',
        },
        geometry: {
          type: 'geo_shape',
        },
      },
    },
  },
}



console.log('Deleting and recreating indices with mapping..')

for (const [indexName, mapping] of Object.entries(indices)) {
  const indexUrl = `${elasticsearchUrlPrefix}${indexName}`

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

  request.put({
    url: `${indexUrl}`,
    json: true,
    body: mapping,
  })
    .then((response) => {
      console.log(`Success: ${indexUrl}`)
      // console.log(response);
    })
    .catch((err) => {
      console.log(`Error: ${indexUrl}`)
      console.log(err.message)
    })
}
