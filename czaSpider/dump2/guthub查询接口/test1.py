import re, pymongo, github.GithubObject

from github import Github
from datetime import datetime, timedelta

from config import account, passwd

MONGO_INFO = {
    "host": 'localhost',
    "port": 27017,
    "document_class": dict
}


def to_datetime(time_obj):
    if isinstance(time_obj, datetime):
        return time_obj
    if re.match('^\d{8}$', time_obj):
        return datetime.strptime(time_obj, '%Y%m%d')
    else:
        return github.GithubObject.NotSet


def process_commands(all=None, size=None, ne=None, gt=None, gte=None, lt=None, lte=None, **kwargs):
    commands = []
    if kwargs:
        commands.append(kwargs)
    if all:  # {key:[v1,v2]}
        commands.append({key: {"$all": value} for key, value in all.items()})
    if size:  # {key:value}
        commands.append({key: {"$size": value} for key, value in size.items()})
    if ne:
        commands.append({key: {"$ne": value} for key, value in ne.items()})
    if gt:
        commands.append({key: {"$gt": value} for key, value in gt.items()})
    if gte:
        commands.append({key: {"$gte": value} for key, value in gte.items()})
    if lt:
        commands.append({key: {"$lt": value} for key, value in lt.items()})
    if lte:
        commands.append({key: {"$lte": value} for key, value in lte.items()})
    query = {"$and": commands} if commands else {}
    return query


def pop_key_from_dict(di):
    res = [k for k in di.keys()]
    return res[0] if len(res) == 1 else res


class Mongodb(object):
    def __init__(self, dbName, collName):
        self.dbName = dbName
        self.collName = collName
        self.client = pymongo.MongoClient(**MONGO_INFO)
        self.database = self.client[dbName]
        self.collection = self.database[collName]
        self._docs = self.collection.count()
        self._documents = None

    @property
    def documents(self):
        res = self._documents
        self._documents = None
        return res

    @property
    def docs(self):
        res = self._docs
        self._docs = None
        return res

    def _count(self):
        self._docs = self.collection.count()

    def count(self, all=None, size=None, ne=None, gt=None, gte=None, lt=None, lte=None, **kwargs):
        query = process_commands(all, size, ne, gt, gte, lt, lte, **kwargs)
        self._docs = self.collection.count(query)
        return self

    def update(self, set=None, unset=None, upsert=False, **kwargs):  # update one document,
        command = dict()
        if set:
            command = {"$set": set}
        elif unset:
            command = {"$unset": set}
        self.collection.update_one(kwargs, command, upsert=upsert)
        self._count()
        return self

    def updateAll(self, set=None, unset=None, upsert=False, **kwargs):
        command = dict()
        if set:
            command = {"$set": set}
        elif unset:
            command = {"$unset": set}
        self.collection.update_many(kwargs or {}, command, upsert=upsert)
        self._count()
        return self

    def insert(self, new_document=None, **kwargs):  # insert_one(dict)3
        self.collection.insert_one(new_document or kwargs)
        self._count()
        return self

    def insertAll(self, new_documents_list: list):  # insert_many(list)
        self.collection.insert_many(new_documents_list)
        self._count()
        return self


class GithubManager:
    def __init__(self, mongodb_info=()):
        self.github = Github(account, passwd)
        self.all_repositories = self.github.get_user().get_repos()
        mongodb_info = mongodb_info if mongodb_info else ('github', 'statistics_by_month')
        self.mongodb = Mongodb(*mongodb_info)

    def get_commit_by_datetime(self, from_time, to_time):
        commit_times = 0
        for repo in self.all_repositories:
            commit_times += repo.get_commits(since=to_datetime(from_time), until=to_datetime(to_time)).totalCount
        return commit_times

    def get_statistics_all_month(self):
        pass

    def get_statistics_current_month(self):
        now = datetime.now()
        year, month = now.year, now.month
        current_month_first_day = datetime(year, month, 1)
        commits = self.get_commit_by_datetime(current_month_first_day, now)
        commit_month = int(current_month_first_day.timestamp())
        documents = {'commit_month': commit_month, 'commit_count': commits}  # 保存当月第一天的时间戳
        self.mongodb.update(commit_month=commit_month, set=documents, upsert=True)

    def get_statistics_appoint_month(self, year=None, month=None):
        now = datetime.now()
        year, month = (year, month) if year and month else (now.year, now.month)
        current_month_first_day = datetime(year, month, 1)
        current_month_last_day = datetime(year, month, 1)


if __name__ == '__main__':
    github_handler = GithubManager()
    # print(github_handler.get_commit_by_datetime('20190401', '20190701'))
    # print(github_handler.get_commit_by_datetime('', ''))

    print(github_handler.get_statistics_current_month())
