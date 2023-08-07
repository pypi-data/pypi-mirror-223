import json

class Streamer():
    def __init__(self, chunk_gen):
        self._chunk_gen = chunk_gen

    def iter_item(self):
        partial_chunk = ''
        for chunk in self._chunk_gen:
            chunk_str = chunk.decode("utf-8")
            if partial_chunk:
                chunk_str = partial_chunk + chunk_str
                partial_chunk = '';
            for item in chunk_str.split('\n\n'):
                try:
                    item_json = json.loads(item)
                    yield item_json
                except:
                    partial_chunk += item
