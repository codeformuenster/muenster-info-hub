import json

from elasticsearch import Elasticsearch

ES_URL = "https://data.mein-ms.de/"


def read_json(path):
    with open(path) as json_file:
        return json.load(json_file)


def post_elastic(content):
    res = Elasticsearch(ES_URL).index(
        index=("infohub"),
        doc_type="_doc",
        body=content
    )


data = read_json('virtualnights.json')

for d in data:
    post_elastic(d)
