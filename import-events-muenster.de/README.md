
## Index init
Delete all content and then recreate the index: 
```bash
node create_indexes.js
```
## Event import
Import the stadt-münster-top-events:

```bash
export ELASTICSEARCH_URL_PREFIX="https://data.mein-ms.de/"
export MAPQUEST_KEY="supersecretkey"
scrapy runspider TopEvents.py
```
