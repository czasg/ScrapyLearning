# todo, 管理文件、下载。 可以调用mongo和redis辅助处理数据
import logging
import requests
import json

from czaSpider.dataBase.config import FID_SERVER

logging = logging.getLogger(__name__)

UPLOAD_URL = FID_SERVER + 'upload/file'
FETCH_URL = FID_SERVER + 'fetch/'


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
                response = json.loads(requests.post(UPLOAD_URL, files={"": doc_bytes}).text)
                self.fid, self.size = response['fid'], response['size']
            except:
                logging.warning('Can Not push file to file-server')
        self.polish()

    def process(self, download=None, close=False):
        if isinstance(self.request, str) and not self.fid:  # str -> bytes -> _upload -> file-server
            self._upload(self.request.encode())
        if isinstance(self.request, dict) and not close and not self.fid:
            self._upload(download(self.request))
        return self

    def fetch_file(self):
        return requests.get(FETCH_URL + self.fid).content if self.fid else b''
