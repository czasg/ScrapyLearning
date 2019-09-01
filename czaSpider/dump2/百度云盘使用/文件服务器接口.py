from bypy import ByPy


class ByPyFileServer:
    def __init__(self, to_path):
        self.bp = ByPy()
        self.to_path = to_path

    def upload(self, file_path):
        self.bp.upload(file_path, self.to_path)

    def download(self, file_name, to_path='/'):
        self.bp.download(to_path, self.to_path + file_name)
