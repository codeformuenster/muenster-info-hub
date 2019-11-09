# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os.path

import os

from elasticsearch import Elasticsearch


http_auth = scheme = None
if 'ELASTICSEARCH_USERNAME' in os.environ and 'ELASTICSEARCH_PASSWORD' in os.environ:
    http_auth = (
        os.environ['ELASTICSEARCH_USERNAME'],
        os.environ['ELASTICSEARCH_PASSWORD']
    )
    scheme = 'https'

if 'ELASTICSEARCH_URL_PREFIX' in os.environ:
    elasticsearch_url, index_prefix = os.environ['ELASTICSEARCH_URL_PREFIX'].rsplit("/", maxsplit=1)
else:
    elasticsearch_url, index_prefix = None, None

class JsonWithEncodingPipeline(object):
    def _post_elastic(self, content):

        # generate unique id for event
        eventId = 'pa_scr_' + content['title'] + content['start_date']
        content['id'] = eventId

        # insert into elasticsearch
        Elasticsearch(elasticsearch_url, http_auth=http_auth, scheme=scheme).index(
            index=(f"{index_prefix}events"),
            doc_type="_doc",
            body=content,
            id=eventId
        )

    def process_item(self, item, spider):
        # if os.path.exists(FILE_NAME):
        #     with open(FILE_NAME, 'r') as json_file:
        #         previous = json.load(json_file)
        #
        #     with open(FILE_NAME, 'w') as json_file:
        #         previous.append(dict(item))
        #         json_file.write(json.dumps(previous, ensure_ascii=False))
        # else:
        #     with open(FILE_NAME, 'w+') as json_file:
        #         json_file.write(json.dumps([dict(item)], ensure_ascii=False))
        if not item:
            return

        if elasticsearch_url:
            self._post_elastic(dict(item))
        return item

    def spider_closed(self, spider):
        pass
