import time

from database.mysql.orm import *
from tools.idgen import id_pool


def next_id(): return id_pool.next_id()


class User(Model):
    __table__ = 'users1'

    id = IntegerField(primary_key=True, default=next_id)
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)
    unread_msg = IntegerField()


class Blog(Model):
    __table__ = 'blogs1'

    id = IntegerField(primary_key=True, default=next_id)
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)', default='/static/img/user.png')
    blog_image = StringField(ddl='varchar(50)')
    title = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)
    count = IntegerField()
    update_at = FloatField(default=time.time)
    blog_type = StringField(ddl='varchar(50)')


class Comment(Model):
    __table__ = 'comments1'

    id = IntegerField(primary_key=True, default=next_id)
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(50)')
    content = TextField()
    created_at = FloatField(default=time.time)


class SonComment(Model):
    __table__ = 'son_comments1'

    id = IntegerField(primary_key=True, default=next_id)
    comment_id = StringField(ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(50)')
    content = TextField()
    created_at = FloatField(default=time.time)
