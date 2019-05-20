import logging
import requests
import json

from czaSpider.dataBase.config import FID_SERVER

logging = logging.getLogger(__name__)

UPLOAD_URL = FID_SERVER + 'upload/file'
FETCH_URL = FID_SERVER + 'fetch/'


class FileManager:
    """
    主要功能，对接文件服务器，包含上传文件、下载文件、数据结构化输出
    上传文件：process + _upload
    下载文件：fetch_file
    数据结构化：polish，对外主要起润色的功能，对输入数据进行结构化处理
    """

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

    def polish(self):
        if isinstance(self.request, str) and self.request.startswith('http'):
            self.request = dict(url=self.request)
        self._requests = dict(request=self.request,
                              fid=self.fid,
                              size=self.size)

    def _upload(self, doc_bytes, drop_request=False):
        if doc_bytes:
            try:
                response = json.loads(requests.post(UPLOAD_URL, files={"": doc_bytes}).text)
                self.fid, self.size = response['fid'], response['size']
                self.request = None if self.fid and drop_request else self.request
            except:
                logging.warning('Can Not push file to file-server')
        self.polish()

    def process(self, download=None, close=False):
        if isinstance(self.request, str) and not self.fid:  # str -> bytes -> _upload -> file-server
            self._upload(self.request.encode(), drop_request=False)
        if isinstance(self.request, dict) and not close and not self.fid:  # dict -> download -> bytes -> _upload -> file-server
            self._upload(download(self.request))
        return self

    def fetch_file(self):
        return requests.get(FETCH_URL + self.fid).content if self.fid else b''
