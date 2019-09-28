import elasticsearch
import os
import json
from datetime import datetime

elasticsearch_url, index_prefix = os.environ['ELASTICSEARCH_URL_PREFIX'].rsplit("/", maxsplit=1)
es = elasticsearch.Elasticsearch(elasticsearch_url)

for file in os.listdir("./data"):
    if file.endswith(".json"):
        print(os.path.join("./data", file))

        with open(os.path.join("./data", file)) as f:
            doc = json.load(f)
            doc["start_date"] = datetime.fromtimestamp(int(doc["date_published"])).isoformat()

            res = es.index(index=f"{index_prefix}events", body=doc)
            print(res['result'])
