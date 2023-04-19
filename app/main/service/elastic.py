from elasticsearch import Elasticsearch
from app.main.service.deep_learning import *

es = Elasticsearch(hosts="http://localhost:9200",verify_certs=False)

def index_document(content, embedding):
    doc = {
        'text': summarization_task(content),
        'vector': embedding
    }
    return es.index(index="vector_test",document=doc)['result']


def index_search(vector_query):
    return es.search(index="vector_test", body={"query": {"script_score": { "query": { "match_all": {}},"script": {"source": "cosineSimilarity(params.query_vector, 'vector') + 1.0","params": {"query_vector": vector_query}}}}})