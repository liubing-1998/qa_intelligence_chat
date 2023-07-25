import json
import os

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from pprint import pprint

class ESClient():

    def __init__(self,
                 host=None,
                 username=str('elastic'),
                 password=str('WdgfOyS=G=nRz1wT+LqJ')):
        if host is None:
            host = {'host': 'localhost', 'port': 9200, "scheme": "http"}
        self.es = Elasticsearch([host], basic_auth=(username, password))

    # 创建索引
    def create_index(self, index_json_name, index_name):
        PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
        index_file_path = os.path.join(PROJECT_ROOT, index_json_name)
        with open(index_file_path) as index_file:
            source = json.load(index_file)
            self.es.indices.create(index=index_name, settings=source["settings"], mappings=source["mappings"])

    # 添加索引记录
    def add_index(self, index_name, doc_id, body):
        # 若当前id已存在，则删除
        self.delete_index(index_name, doc_id)
        # 添加索引记录
        self.es.index(index=index_name, id=doc_id, body=body)

    # 批量添加索引记录
    def bulk_add_index(self, docs):
        '''
        :param docs: 按照es格式处理好的json格式
        :return:
        '''
        bulk(self.es, docs)

    # 删除索引记录
    def delete_index(self, index_name, doc_id):
        if self.es.exists(index=index_name, id=doc_id):
            self.es.delete(index=index_name, id=doc_id)

    def search_documents(self, index_name, query, top_n):
        # 执行查询
        response = self.es.search(
            index=index_name, size=top_n, query=query, source_includes=["title", "text"]
        )
        pprint(response)

        for hit in response['hits']['hits']:
            print(hit)
        return response['hits']['hits']
