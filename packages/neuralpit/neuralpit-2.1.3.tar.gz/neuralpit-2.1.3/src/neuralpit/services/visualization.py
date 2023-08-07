import requests
from typing import List
import json
from requests.compat import urljoin
from neuralpit import NeuralPitSDK, STREAM_DELIMITER
from neuralpit.utils.streamer import Streamer

class VisualizationnService():

    def __init__(self) -> None:
        super().__init__()
        sdk = NeuralPitSDK.instance()
        self.api_key = sdk.api_key
        self.api_endpoint = sdk.api_endpoint

    def updateConversationDatasourceFromS3(self, conversation_id, bucket: str, key:str):
        put_url = urljoin(self.api_endpoint,f'/visualization/{conversation_id}/s3_datasource')
        headers = {'x-api-key':self.api_key, 'Content-Type':'application/json'}
        put_call = requests.post(put_url, headers = headers, json = {'bucket': bucket, 'key': key})
        resp =  json.loads(put_call.content)
        return resp
    

    def summarizeDatasource(self, conversation_id, chunk_size=1024):
        post_url = urljoin(self.api_endpoint,f'/visualization/{conversation_id}/datasource/summarize')
        headers = {'x-api-key':self.api_key}
        with requests.post(post_url, headers = headers, stream=True) as r:
            yield from r.iter_content(chunk_size)
