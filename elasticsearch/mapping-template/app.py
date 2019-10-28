import elasticsearch
import os
import json

elasticsearch_url, index_prefix = os.environ["ELASTICSEARCH_URL_PREFIX"].rsplit("/", maxsplit=1)

http_auth = scheme = None
if 'ELASTICSEARCH_USERNAME' in os.environ and 'ELASTICSEARCH_PASSWORD' in os.environ:
    http_auth = (
        os.environ['ELASTICSEARCH_USERNAME'],
        os.environ['ELASTICSEARCH_PASSWORD']
    )
    scheme = 'https'

es = elasticsearch.Elasticsearch(elasticsearch_url, http_auth=http_auth, scheme=scheme)

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

# FIXME log success/error