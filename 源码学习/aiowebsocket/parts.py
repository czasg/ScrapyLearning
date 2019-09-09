from urllib.parse import urlparse
from collections import namedtuple

REMOTE = namedtuple('REMOTE', ['scheme', 'host', 'port', 'resource', 'ssl'])


def parse_uri(uri: str):  # 用来解析url的
    uri = urlparse(uri)
    try:
        scheme = uri.scheme
        host = uri.hostname
        port = uri.port or (443 if scheme == 'wss' else 80)
        ssl = True if scheme == 'wss' else False
        resource = uri.path or '/'
        if uri.query:
            resource += '?' + uri.query
    except AssertionError as exc:
        raise ValueError("The '{uri}' unverified".format(uri=uri)) from exc
    return REMOTE(scheme, host, port, resource, ssl)


if __name__ == '__main__':
    remote = parse_uri('http://192.168.0.110:3030/credit/criditone_test.html?name=null&type=null&page=news')
    # REMOTE(
    # scheme='http',
    # host='192.168.0.110',
    # port=3030,
    # resource='/credit/criditone_test.html?name=null&type=null&page=news',
    # ssl=False
    # )
