import datetime
import os

import editdistance
from elasticsearch import Elasticsearch


http_auth = scheme = None
if (
    ('ELASTICSEARCH_USERNAME' in os.environ) and
    ('ELASTICSEARCH_PASSWORD' in os.environ)):
    http_auth = (
        os.environ['ELASTICSEARCH_USERNAME'],
        os.environ['ELASTICSEARCH_PASSWORD']
    )
    scheme = 'https'

if 'ELASTICSEARCH_URL_PREFIX' in os.environ:
    elasticsearch_url, index_prefix = (os.environ['ELASTICSEARCH_URL_PREFIX']
        .rsplit("/", maxsplit=1))
else:
    elasticsearch_url, index_prefix = None, None


es = Elasticsearch(elasticsearch_url, http_auth=http_auth, scheme=scheme)

def _events_by_day(date):
    '''query all events by day from ES'''
    res = es.search(
        index=(f'{index_prefix}events'),
        body={
            "query": {
                "bool": {
                    "filter": [
                        { "term":
                            {"start_date":
                                { "value": date.strftime('%Y-%m-%d')}
                            }
                        }
                    ]
                }
            }
        }
    )

    data = res['hits']['hits']
    return [d['_source'] for d in data]


def _compare(string1, string2):
    return editdistance.eval(string1, string2)

def _normalize_str(string):
    " ".join(foo.split())
    string = string.lower()
    # string.replace(old, new)

    return string


if __name__ == "__main__":
    date = datetime.date(year=2019, month=11, day=9)
    print(_events_by_day(date))
