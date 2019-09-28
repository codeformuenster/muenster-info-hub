# muenster-info-hub


start elasticsearch
```bash
export COMPOSE_PROJECT_NAME="msinfohub"
export ELASTICSEARCH_URL_PREFIX="http://elasticsearch:9200/msinfohub-"

docker-compose up
```

```bash
# ip for elasticsearch
elasticsearch_ip=$(docker network inspect msinfohub_default | jq -r '.[].Containers | to_entries[] | select(.value.Name=="'"$COMPOSE_PROJECT_NAME"'_elasticsearch_1") | .value.IPv4Address | split("/")[0]')
echo "xdg-open http://$elasticsearch_ip:9200"

# ip for kibana
kibana_ip=$(docker network inspect msinfohub_default | jq -r '.[].Containers | to_entries[] | select(.value.Name=="'"$COMPOSE_PROJECT_NAME"'_kibana_1") | .value.IPv4Address | split("/")[0]')
echo "xdg-open http://$kibana_ip:5601"
```


```bash
# delete index
curl --request DELETE "http://$elasticsearch_ip:9200/msinfohub-*"

```

## Datenstruktur

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

