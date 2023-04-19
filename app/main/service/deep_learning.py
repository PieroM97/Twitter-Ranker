import transformers
from transformers import AutoTokenizer, AutoModel, BartTokenizer, BartForConditionalGeneration, \
    AutoModelForQuestionAnswering
from transformers import pipeline
from app.main.service.helper import *
import requests
import torch
import torch.nn.functional as F


MODEL_SUMMARIZATION = f"philschmid/flan-t5-base-samsum"
MODEL_URL = "https://api-inference.huggingface.co/models/philschmid/bart-large-cnn-samsum"
MODEL_URL_QA = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

def prepare_request_for_huggingface():
    keys = load_keys()
    API_TOKEN = keys["api_token_huggingface"]
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    return headers
def pipeline(payload,model_url):
    headers = prepare_request_for_huggingface()
    data = json.dumps(payload)
    response = requests.request("POST", model_url, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


#Summarization
def text_segmentation(full_text, dim = 12560):
    list_of_text = [full_text[i:i + dim] for i in range(0, len(full_text), dim)]
    return list_of_text
def summarization_task(text):

    final_text = ""
    list_of_text = text_segmentation(text)
    for segment in list_of_text:
        result = pipeline(segment,MODEL_URL)
        final_text = final_text + result[0]['summary_text']
    return final_text

#Vector search
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
def text_embedding(text):
    # Load model from HuggingFace Hub
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

    # Tokenize sentences
    encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    # Perform pooling
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # Normalize embeddings
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

    return sentence_embeddings.numpy().tolist()[0]

#Question answering
def question_answering(context,question):
    qa_payload = f"question: {question} context: {context['hits']['hits'][0]['_source']['text']}"
    model_name = "deepset/roberta-base-squad2"

    
    nlp = transformers.pipeline('question-answering', model=model_name,tokenizer=model_name)
    result = nlp(qa_payload)
    return result['answer']

#Chatbot answering like
def chat_answering(context,question):
    tokenizer = BartTokenizer.from_pretrained("vblagoje/bart_lfqa")
    model = BartForConditionalGeneration.from_pretrained("vblagoje/bart_lfqa").to("cpu")
    query = f"question: {question} context: {context}"

    inputs = tokenizer([query],max_length=512,return_tensors="pt",truncation=True,stride=100)

    ids = model.generate(inputs["input_ids"],do_sample=False,num_beams=8,no_repeat_ngram_size=3,num_return_sequences=1,max_length=40)
    return tokenizer.batch_decode(ids,skip_special_tokens=True,clean_up_tokenization_spaces=True)[0]