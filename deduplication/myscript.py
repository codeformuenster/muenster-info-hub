import datetime
import os
from itertools import combinations

import textdistance
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
    # events = [(e['title'], for e in _events_by_day(date)]
    events = _events_by_day(date)

    # uses lcsseq in relation to length of strings. value < ~1.1 is likely duplicate
    two_tuples = combinations(events, r=2)
    two_tuples = [(
        t[0], t[1], (
            min(len(t[0]['title']), len(t[1]['title'])) / len(textdistance.lcsseq(t[0]['title'], t[1]['title'])) +
            min(len(t[0]['location_name']), len(t[1]['location_name'])) / len(textdistance.lcsseq(t[0]['location_name'], t[1]['location_name']))) / 2) for t in two_tuples]

    two_tuples.sort(key=lambda x: x[2])

    for t in two_tuples:
        print('[{} / {}], [{} / {}] -> {}'
            .format(
                t[0]['title'],
                t[1]['title'],
                t[0]['location_name'],
                t[1]['location_name'],
                t[2]
            )
        )

    # TODO: decide which duplicate to delete (prob. the one with "less" data)
    # TODO: find way of deploying and running (Cronjob?)