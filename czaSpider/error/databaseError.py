from czaSpider.error.baseError import baseError


class ConnectError(baseError):
    def __init__(self, field, message='database can not connect, check server'):
        super(ConnectError, self).__init__('db: Invalid', field, message)

# try:
#     raise ConnectError('mongodb')
# except ConnectError as e:
#     print(e.error)
#     print(e.field)
#     print(e.message)
