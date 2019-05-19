import requests


class BaseDownloader:
    def __init__(self, **kwargs):
        pass

    def download(self, request: dict) -> bytes:  # todo, add middleware to polish request or response
        req = request.copy()

        response = requests.request('GET', req['url'])

        content = response.content

        return content
