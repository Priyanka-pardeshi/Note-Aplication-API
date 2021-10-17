from elasticsearch import Elasticsearch
from django.conf import settings

'''
    Performing get, post, delete operation on data Using Elastic search.
'''


class Elastic_search:
    def __init__(self):
        self.es = Elasticsearch(hosts=settings.ES_HOST, port=settings.ES_PORT)

    def post_data(self, note_data):
        es_data = self.es.index(index="note", id=1, body=note_data)
        return es_data['result']

    def get_data(self, user_id):
        query = {
            "query": {
                "term": {
                    "user_id": user_id
                }
            }
        }
        data = self.es.search(index="note", body=query)
        list_data = data['hits']['hits']
        note_list = []
        for data in list_data:
            print(data.get("_source"), " :data")
            note_list.append(data.get("_source"))
        return note_list

    def delete_data(self, note_name):
        query = {
            "query": {
                "match": {
                    "title": note_name
                }
            }
        }
        self.es.delete_by_query(index="note", body=query)
