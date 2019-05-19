class baseError(Exception):
    def __init__(self, error, field='', message=''):
        super(baseError, self).__init__(message)
        self.error = error
        self.field = field
        self.message = message

