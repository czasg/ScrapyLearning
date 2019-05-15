class baseError(Exception):
    def __init__(self, error, data='', message=''):
        super(baseError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message

