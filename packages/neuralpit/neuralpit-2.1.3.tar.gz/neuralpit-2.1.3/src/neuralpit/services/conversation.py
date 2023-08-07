import requests
from typing import List
import json
from requests.compat import urljoin
from neuralpit import NeuralPitSDK, STREAM_DELIMITER
from neuralpit.utils.streamer import Streamer

class ConversationService():

    def __init__(self) -> None:
        super().__init__()
        sdk = NeuralPitSDK.instance()
        self.api_key = sdk.api_key
        self.api_endpoint = sdk.api_endpoint


    def createConversation(self, conversation):
        print(conversation)
        post_url = urljoin(self.api_endpoint,'/conversation')
        headers = {'x-api-key':self.api_key, 'Content-Type':'application/json'}
        post_call = requests.post(post_url, headers = headers, json = {'conversation': conversation})
        resp =  json.loads(post_call.content)
        return resp
    
    def deleteConversation(self, conversation_id):
        delete_url = urljoin(self.api_endpoint,f'/conversation/{conversation_id}')
        headers = {'x-api-key':self.api_key, 'Content-Type':'application/json'}
        delete_call = requests.delete(delete_url, headers = headers)
        return True
    
    def addConversationDocumentFromS3(self, conversation_id, bucket, keys:List[str]):
        post_url = urljoin(self.api_endpoint,f'/conversation/{conversation_id}/s3_document')
        headers = {'x-api-key':self.api_key, 'Content-Type':'application/json'}
        post_call = requests.post(post_url, headers = headers, json = [{'bucket': bucket, 'key': key} for key in keys])
        resp =  json.loads(post_call.content)
        return resp
    
    def addConversationDocumentFromUrl(self, conversation_id, url:str, mode: str):
        post_url = urljoin(self.api_endpoint,f'/conversation/{conversation_id}/web_document')
        headers = {'x-api-key':self.api_key, 'Content-Type':'application/json'}
        post_call = requests.post(post_url, headers = headers, json = {'url': url, 'mode': mode})
        resp =  json.loads(post_call.content)
        return resp
    
    def deleteConversationDocument(self, conversation_id, document_id):
        delete_url = urljoin(self.api_endpoint,f'/conversation/{conversation_id}/document/{document_id}')
        headers = {'x-api-key':self.api_key, 'Content-Type':'application/json'}
        delete_call = requests.delete(delete_url, headers = headers)
        return True
    
    def listConversationDocument(self, conversation_id):
        get_url = urljoin(self.api_endpoint,f'/conversation/{conversation_id}/document')
        headers = {'x-api-key':self.api_key, 'Content-Type':'application/json'}
        get_call = requests.get(get_url, headers = headers)
        resp =  json.loads(get_call.content)
        return resp
    
    def listConversationHistory(self, conversation_id):
        get_url = urljoin(self.api_endpoint,f'/conversation/{conversation_id}/history')
        headers = {'x-api-key':self.api_key, 'Content-Type':'application/json'}
        get_call = requests.get(get_url, headers = headers)
        resp =  json.loads(get_call.content)
        return resp
    
    def clearConversationHistory(self, conversation_id):
        delete_url = urljoin(self.api_endpoint,f'/conversation/{conversation_id}/history')
        headers = {'x-api-key':self.api_key, 'Content-Type':'application/json'}
        delete_call = requests.delete(delete_url, headers = headers)
        return True
    
    def clearConversationDocuments(self, conversation_id):
        delete_url = urljoin(self.api_endpoint,f'/conversation/{conversation_id}/document')
        headers = {'x-api-key':self.api_key, 'Content-Type':'application/json'}
        delete_call = requests.delete(delete_url, headers = headers)
        return True

    
    def summarizeDocument(self, conversation_id, document_id, debug=False):
        get_url = urljoin(self.api_endpoint,f'/conversation/{conversation_id}/document/{document_id}/summarize')
        headers = {'x-api-key':self.api_key, 'Content-Type':'application/json'}
        get_call = requests.get(get_url, headers = headers, json = {'debug': debug})
        return get_call.content
    
    def queryConversation(self, conversation_id, question, debug=False, chunk_size=1024):
        post_url = urljoin(self.api_endpoint,f'/conversation/{conversation_id}/query')
        headers = {'x-api-key':self.api_key}
        with requests.post(post_url, headers = headers, json = {'question': question, 'debug': debug}, stream=True) as r:
            streamer = Streamer(r.iter_content(chunk_size))
            for item in streamer.iter_item():
                yield item

    def queryIdea(self, conversation_id, question, debug=False, chunk_size=1024):
        post_url = urljoin(self.api_endpoint,f'/conversation/{conversation_id}/idea')
        headers = {'x-api-key':self.api_key}
        with requests.post(post_url, headers = headers, json = {'question': question, 'debug': debug}, stream=True) as r:
            streamer = Streamer(r.iter_content(chunk_size))
            for item in streamer.iter_item():
                yield item