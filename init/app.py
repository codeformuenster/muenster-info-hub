import elasticsearch
import os
import json

elasticsearch_url, index_prefix = os.environ["ELASTICSEARCH_URL_PREFIX"].rsplit("/", maxsplit=1)
es = elasticsearch.Elasticsearch(elasticsearch_url)

with open("mapping.json") as f:
    doc = json.load(f)

    template = {
        "index_patterns": [f"{index_prefix}*"],
        "mappings": {
            "properties": doc
        }
    }

    es.indices.put_template(
        name=f"{index_prefix}events",
        body=template
    )
