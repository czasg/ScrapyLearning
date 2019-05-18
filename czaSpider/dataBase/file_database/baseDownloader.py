# todo， 此处应包含实际的文件下载逻辑
import logging
import requests

logging = logging.getLogger(__name__)


class Record(dict):
    def __init__(self, **kwargs):
        super(Record, self).__init__(**kwargs)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


class BaseDownloader:
    def __init__(self, **kwargs):
        pass

    def download(self, request: dict) -> bytes:  # todo, add middle pipe to polish request
        req = request.copy()

        response = requests.request('GET', req['url'])

        content = response.content

        return content
