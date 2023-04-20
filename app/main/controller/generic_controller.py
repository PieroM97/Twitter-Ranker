from flask import Blueprint, request


from app.main.service.crawler import *
from app.main.service.deep_learning import *
from app.main.service.elastic import *



from trafilatura.spider import focused_crawler


Controller_blueprint = Blueprint("Controller_blueprint", __name__)

#Indexation

@Controller_blueprint.post("/crawl/summerize")
def postSummerize():

  url = request.get_json()['url']
  content = getSinglePage(url)

  return summarization_task(content),200

@Controller_blueprint.post("/crawl/embedding")
def postEmbedding():

  url = request.get_json()['url']

  content = getSinglePage(url)
  embedding = text_embedding(content)

  result = index_document(content,embedding)

  return result,200


#Search

@Controller_blueprint.post("/vector_search")
def postSearch():

  query = request.get_json()['query']
  vector_query =  text_embedding(query)
  return index_search(vector_query).body,200


@Controller_blueprint.post("/question_answering")
def postQuestion():

  query = request.get_json()['query']
  vector_query =  text_embedding(query)
  answer = question_answering(index_search(vector_query).body,query)
  return answer,200


@Controller_blueprint.post("/chatbot")
def postChatbot():
    query = request.get_json()['query']
    vector_query = text_embedding(query)
    answer = chat_answering(index_search(vector_query).body, query)
    return answer, 200