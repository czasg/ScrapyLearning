import logging

from collections import defaultdict

from pyws.snow_key import id_pool

logger = logging.getLogger(__name__)


class Connector:
    def __init__(self, request, client_address, name=None):
        self.request = request
        self.client_address = ':'.join([str(i) for i in client_address])
        if name:
            self.name = name
            self.clear_level = 0
        else:
            self.name = str(id_pool.next_id())
            self.clear_level = 1


class ConnectManager:
    connectors = defaultdict(dict)
    groups = defaultdict(dict)

    @classmethod
    def online(cls):
        return len(cls.connectors)

    @classmethod
    def clear(cls, name, key, clear_level=0):
        if key in cls.connectors[name]:
            if clear_level:
                cls.connectors.pop(name)
            else:
                cls.connectors[name].pop(key)

    @classmethod
    def add_connector(cls, name, key, value):
        cls.connectors[name][key] = value

    @classmethod
    def add_group(cls, name, key, value):
        cls.groups[name][key] = value

    @classmethod
    def group_exist(cls, key):
        return key in cls.groups

    @classmethod
    def group_exist_key(cls, name, key):
        return key in cls.groups[name]

    @classmethod
    def send_to_connector(cls, name, msg):
        try:
            for connector in cls.connectors[name].values():
                connector.request.ws_send(msg)
            logger.info('发送成功')
            return 1
        except:
            return 0

    @classmethod
    def next_user(cls):
        yield from (connector for connectors in cls.connectors.values()
                    for connector in connectors.values())
