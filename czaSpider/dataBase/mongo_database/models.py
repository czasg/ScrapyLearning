from .orm import SourceDB, ResolverDB


class Mongodb:
    def __init__(self, dbName, collName, parse_item=False):
        self.source = SourceDB(dbName, collName, parse_item)
        self.resolver = ResolverDB(dbName, collName)
