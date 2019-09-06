from urllib.parse import urlparse
from collections import namedtuple

REMOTE = namedtuple('REMOTE', ['scheme', 'host', 'port', 'resource', 'ssl'])


def parse_uri(uri: str):
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
