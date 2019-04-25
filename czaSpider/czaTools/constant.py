SOURCE = "save-source"
SAVED_SOURCE_NAME = "sourceItem"

post_dict = dict(method="POST", headers={'Content-Type': 'application/x-www-form-urlencoded'})

# sql
SQL_CREATE_TABLE = """create table if not exists source (
author varchar(10), 
more varchar(200), 
releaseTime varchar(20), 
source varchar(200), 
spiderName varchar(100), 
url varchar(100))"""

SQL_INSERT_TABLE = """insert into source values ({},{},{},{},{},{})"""
