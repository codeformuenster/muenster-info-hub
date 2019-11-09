# muenster-info-hub

## Project info

Created during MünsterHack 2019. Searchengine and open API for Münster related events.

Directories: 

* `elasticsearch` - Elasticsearch related files
* `import`- Import-scripts for the various event sources. Run periodically to import events into the elasticsearch database
* `html` - Html-content for production. Will be served via the corresponding subdomains on the webserver
  * Content of the directory _app.muenster-jetzt.de_ is generated via the repository "muenster-info-app": https://github.com/codeformuenster/muenster-info-app 


## Start developing

start elasticsearch
```bash
cd elasticsearch
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

# import partyphase and virtualnights
cd ./party_scraper
docker-compose up --build ODER
SCRAPE_START=yyyy-mm-dd SCRAPE_END=yyyy-mm-dd docker-compose up --build

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

The index name that we currently use in production is: **msinfohub-events**

* Show indexes: https://api.muenster.jetzt/_cat/indices
* Mapping anzeigen: https://api.muenster.jetzt/infohub/_mapping
* Show content of mein-ms-places index: https://api.muenster.jetzt/infohub/_search
* Search for something: https://api.muenster.jetzt/infohub/_search?q=something
* Search in a specific field: https://api.muenster.jetzt/msinfohub-events/_search?q=field:something
* Sort the searchresults: https://api.muenster.jetzt/msinfohub-events/_search?sort=start_date
* Limit number of results: https://api.muenster.jetzt/msinfohub-events/_search?size=10

### Elasticsearch Query Anleitung 
Man muss nicht unbedingt komplexe JSON-Queries an Elasticsearch schicken, sondern man kann auch viel durch simple GET-Requests erreichen.

Wie die Abfragesprache im Parameter “q” funktioniert: 
https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html
Hier steht wie man nur einzelne Felder zurückbeommt:
https://www.elastic.co/guide/en/elasticsearch/reference/7.3/docs-get.html#docs-get

### Beispiel-Query: 
https://api.muenster.jetzt/infohub/_search?_source=source,geo,start_date&size=200&q=start_date:%3Enow

Erklärung der Beispiel-Query: 
 * Parameter "q" fragt in diesem Fall nur Events ab, die _start_date_ in der Zukunft haben
 * Wegen "_source"-Parameter werden nur die Felder source, geo, start_date zurückgegeben 
 * Durch "size" werden maximal 200 results returnt 

## Elasticsearch fortgeschrittene Aktionen

Query per curl absenden mit der suche nach einem bestimmten Wert in einem bestimmten Feld:

    curl -X POST https://api.muenster.jetzt/msinfohub-events/_search?pretty -H 'Content-Type: application/json' -d'{"query":{"term":{"source":"meinestadt.de"}}}'

    # Alle Einträge einer Eventquelle löschen:
    curl -X POST https://api.muenster.jetzt/msinfohub-events/_delete_by_query?pretty -H 'Content-Type: application/json' -d'{"query":{"term":{"source":"meinestadt.de"}}}'