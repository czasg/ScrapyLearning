class BaseError(Exception):
    def __init__(self, error, field='', message=''):
        super(BaseError, self).__init__(message)
        self.error = error
        self.field = field
        self.message = message


class MySQLExecuteError(BaseError):
    def __init__(self, field, message=''):
        super(MySQLExecuteError, self).__init__('database:execute-error', field, message)

class PrimaryKeyDuplicated(BaseError):
    def __init__(self, field, message=''):
        super(PrimaryKeyDuplicated, self).__init__('database:primary-duplicated', field, message)

class PrimaryKeyUndefined(BaseError):
    def __init__(self, field, message=''):
        super(PrimaryKeyUndefined, self).__init__('database:primary-undefined', field, message)

class APIResourceError(BaseError):
    def __init__(self, field, message=''):
        super(APIResourceError, self).__init__('value:not-found', field, message)

