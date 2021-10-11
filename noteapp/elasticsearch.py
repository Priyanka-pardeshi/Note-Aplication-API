from elasticsearch import Elasticsearch
from django.conf import settings

'''
    Performing get, post, delete operation on data Using Elastic search.
'''


class Elastic_search:
    def __init__(self):
        self.es = Elasticsearch(hosts=settings.ES_HOST, port=settings.ES_PORT)

    def post_data(self):
        note={"title":"notes", "description": "hii", "user_id": 2, "id": 1}
        es_data = self.es.index(index="note", id=1, body=note)
        return es_data['result']

    def get_data(self):
        query = {
            "query": {
                "term": {
                    "title": "elastic notes"
                }
            }
        }
        data = self.es.search(index="note", body=query)
        return data['hits']['hits']

    def delete_data(self):
        query = {
            "query": {
                "match": {
                    "id": "1"
                }
            }
        }
        self.es.delete(index="my_elastic_search", body=query)
