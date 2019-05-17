from .orm import SourceDB, ResolverDB


class Mongodb:
    def __init__(self, dbName, collName):
        self.source = SourceDB(dbName, collName)
        self.resolver = ResolverDB(dbName, collName)
