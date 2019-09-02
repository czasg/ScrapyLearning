import re, pymongo, calendar, github.GithubObject

from github import Github  # pip install PyGithub
from datetime import datetime, timedelta

from config import account, passwd, MONGO_INFO


def to_datetime(time_obj):
    if isinstance(time_obj, datetime):
        return time_obj
    if re.match('^\d{8}$', time_obj):
        return datetime.strptime(time_obj, '%Y%m%d')
    else:
        return github.GithubObject.NotSet


class Mongodb(object):
    def __init__(self, dbName, collName):
        self.dbName = dbName
        self.collName = collName
        self.client = pymongo.MongoClient(**MONGO_INFO)
        self.database = self.client[dbName]
        self.collection = self.database[collName]

    def update(self, set=None, unset=None, upsert=False, **kwargs):  # update one document,
        command = dict()
        if set:
            command = {"$set": set}
        elif unset:
            command = {"$unset": set}
        self.collection.update_one(kwargs, command, upsert=upsert)


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

    def update_commits_count_to_mongodb(self, start, end):
        current_month_first_day = datetime(start, end, 1)
        current_month_last__day = datetime(start, end, calendar.monthrange(start, end)[1])
        commits = self.get_commit_by_datetime(current_month_first_day, current_month_last__day)
        commit_month = int(current_month_first_day.timestamp())
        documents = {'commit_month': commit_month, 'commit_count': commits}  # 保存当月第一天的时间戳
        self.mongodb.update(commit_month=commit_month, set=documents, upsert=True)

    def get_statistics_all_month(self, start_year):
        now = datetime.now()
        current_year, current_month = now.year, now.month
        while start_year <= current_year:
            for month in range(1, 13):
                if month == current_month and start_year == current_year:
                    break
                self.update_commits_count_to_mongodb(start_year, month)
            start_year += 1

    def get_statistics_appoint_month(self, year=None, month=None):
        now = datetime.now()
        year, month = (year, month) if year and month else (now.year, now.month)
        self.update_commits_count_to_mongodb(year, month)


if __name__ == '__main__':
    github_handler = GithubManager()
    # github_handler.get_statistics_appoint_month()
    github_handler.get_statistics_all_month(2019)
