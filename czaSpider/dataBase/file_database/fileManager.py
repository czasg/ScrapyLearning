# todo, 管理文件、下载。 可以调用mongo和redis辅助处理数据
import logging
import requests
import json

from czaSpider.dataBase.config import FID_SERVER

URL = FID_SERVER + 'upload/file'
logging = logging.getLogger(__name__)

# todo, 对外就是一个润色的功能，在downloader里面其主要作用
class FileManager:
    def __init__(self, **kwargs):
        self.request = kwargs.pop("request", None) or kwargs.pop("url", None)
        self.fid = kwargs.pop("fid", None)
        self.size = kwargs.pop("size", None)

        self._requests = None
        self.polish()

    @property
    def requests(self):
        res = self._requests
        self._requests = None
        return res

    def polish(self):  # request is url -> dict
        if isinstance(self.request, str) and self.request.startswith('http'):
            self.request = dict(url=self.request)
        self._requests = dict(request=self.request,
                              fid=self.fid,
                              size=self.size)

    def _upload(self, doc_bytes):
        if doc_bytes:
            try:
                response = json.loads(requests.post(URL, files={"": doc_bytes}).text)
                self.fid, self.size = response['fid'], response['size']
            except:
                logging.warning('Can Not push file to file-server')
        self.polish()

    def process(self, download=None, close=False):
        if isinstance(self.request, str):  # str -> bytes -> _upload -> file-server
            self._upload(self.request.encode())
            self.request = 'done'
        if isinstance(self.request, dict) and not close:
            self._upload(download(self.request))
        return self
