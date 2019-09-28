# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os.path

from elasticsearch import Elasticsearch

ES_URL = "https://data.mein-ms.de/"
FILE_NAME = 'scraped_data_utf8.json'


class JsonWithEncodingPipeline(object):
    def _post_elastic(self, content):
        Elasticsearch(ES_URL).index(
            index=("infohub"),
            doc_type="_doc",
            body=content
        )

    def process_item(self, item, spider):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, 'r') as json_file:
                previous = json.load(json_file)

            with open(FILE_NAME, 'w') as json_file:
                previous.append(dict(item))
                json_file.write(json.dumps(previous, ensure_ascii=False))
        else:
            with open(FILE_NAME, 'w+') as json_file:
                json_file.write(json.dumps([dict(item)], ensure_ascii=False))

        # self._post_elastic(dict(item))
        return item

    def spider_closed(self, spider):
        pass
