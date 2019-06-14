class BaseError(Exception):
    def __init__(self, field, error='', message=''):
        super(BaseError, self).__init__(message)
        self.field = field
        self.error = error
        self.message = message


class MySQLExecuteError(BaseError):
    def __init__(self, error, message=''):
        super(MySQLExecuteError, self).__init__('database:MySQL', error, message)

class PrimaryKeyDuplicated(BaseError):
    def __init__(self, error, message=''):
        super(PrimaryKeyDuplicated, self).__init__('database:primary-duplicated', error, message)

class PrimaryKeyUndefined(BaseError):
    def __init__(self, error, message=''):
        super(PrimaryKeyUndefined, self).__init__('database:primary-undefined', error, message)

class APIResourceError(BaseError):
    def __init__(self, error, message=''):
        super(APIResourceError, self).__init__('value:not-found', error, message)

class APIResourceDeplicated(BaseError):
    def __init__(self, error, message=''):
        super(APIResourceDeplicated, self).__init__('dataLduplicated', error, message)
