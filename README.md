# muenster-info-hub


start elasticsearch
```bash
export COMPOSE_PROJECT_NAME="msinfohub"
export ELASTICSEARCH_URL_PREFIX="http://elasticsearch:9200/msinfohub-"

docker-compose up
```

```bash
# optional

# ip for elasticsearch
export ELASTICSEARCH_IP=$(docker network inspect msinfohub_default | jq -r '.[].Containers | to_entries[] | select(.value.Name=="'"$COMPOSE_PROJECT_NAME"'_elasticsearch_1") | .value.IPv4Address | split("/")[0]')
echo "xdg-open http://$ELASTICSEARCH_IP:9200"

# ip for kibana
export KIBANA_IP=$(docker network inspect msinfohub_default | jq -r '.[].Containers | to_entries[] | select(.value.Name=="'"$COMPOSE_PROJECT_NAME"'_kibana_1") | .value.IPv4Address | split("/")[0]')
echo "xdg-open http://$KIBANA_IP:5601"
```


```bash
# delete index
docker run --network msinfohub_default curlimages/curl:7.65.3 \
  curl --request DELETE "$ELASTICSEARCH_URL_PREFIX*"

# put mapping template
cd ./mapping-template
docker-compose up --build

# import meinestadt
cd ./meinestadt
docker-compose up --build

# import-events-muenster.de
export MAPQUEST_KEY="FIXME"
cd ./import-events-muenster.de
docker-compose up --build

# import partyphase
cd ./party_scraper
docker-compose up --build

# import wn
cd ./import/wn
docker-compose up --build
```

## Datenstruktur

```
{
    "title", 
    "subtitle", // (optional) 
    "start_date": "2008-03-01T13:00:00Z", 
    "end_date": "2008-03-01T15:00:00Z",  // (optional)
    "description", // (optional)
    "link", 
    "category", // (optional)
    "location_name", 
    "location_address",  // (optional)
    "source", // origin of these data
    "tags": [ // (optional)
        "bla", ...
    ],
    "geo": {
        "lat": "51.956944",
        "lon": "7.005556"
        },
    "images":[
        {
        "image_url",  // (optional)
        "image_text", // (optional)
        "image_copyright"    // (optional)
        }
    ],  // (optional)
}
```

## Elasticsearch/API debuggen: 

* Mapping anzeigen: https://api.muenster.jetzt/infohub/_mapping
* Show indexes: https://api.muenster.jetzt/infohub/_cat/indices
* Show content of mein-ms-places index: https://api.muenster.jetzt/infohub/_search
* Search for something: https://api.muenster.jetzt/infohub/_search?q=something
* Search in a specific field: https://api.muenster.jetzt/infohub/_search?q=field:something
