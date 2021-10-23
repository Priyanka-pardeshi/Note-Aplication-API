#from elasticsearch import Elasticsearch
from django.conf import settings
#from elasticsearch.helpers import scan

'''
    Performing get, post, delete operation on data Using Elastic search.
'''


class Elastic_search:
    def __init__(self):
        self.es = Elasticsearch(hosts=settings.ES_HOST, port=settings.ES_PORT)

    def post_data(self, note_data):

        id_list = []
        get_data_record = self.get_all_records()
        print("all data:", get_data_record)
        for data in get_data_record:
            id_list.append(data.get('_id'))

        print("list of id:",id_list)
        max_id=max(id_list)
        print("max id",max_id)
        current_id =int(max_id) + 1
        print("current",current_id,max_id)
        #es_data=self.es.index(index="note",id=current_id,body=note_data)
        es_data = self.es.index(index="note", id=str(current_id), document=note_data)
        print(es_data)
        return es_data['result']

    def get_data(self):
        query = {
            "query": {
                "match_all": {
                }
            }
        }
        data = self.es.search(index="note", body=query)
        print("Object data:", data)
        list_data = data['hits']['hits']
        print("List of dta:", list_data)
        note_list = []
        for data in list_data:
            print(data.get("_source"), " :data")
            note_list.append(data.get("_source"))
        return note_list

    def delete_data(self, note_id):
        get_records = self.get_all_records()
        print(get_records)
        id_list = []
        for data in get_records:
            id_list.append(data.get('_id'))
        print(id_list, "note_id", note_id)
        for note_id in id_list:
            query = {
                "query": {
                    "term": {
                        "_id": note_id
                    }
                }
            }
            self.es.delete_by_query(index="note", body=query)
            return "Record Successfully Deleted"
        return "Record does not exists"

    def get_all_records(self):
        query = {
            "query": {
                "match_all": {}
            }
        }
        es_data = self.es.search(index="note", body=query)
        return es_data['hits']['hits']
