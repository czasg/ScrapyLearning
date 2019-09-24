import os, re, time, base64

from datetime import datetime

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')


def get_file_path(file): return os.path.dirname(os.path.abspath(file))


def to_path(path, *paths): return os.path.join(path, *paths)


def get_now_datetime():
    __date = datetime.now()
    return datetime(__date.year, __date.month, __date.day)


def get_now_time_stamp(): return int(time.time())


def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'),
                filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


def save_image(unique_id, image_body):
    picture = str(unique_id) + '.png'
    with open(to_path(image_path, picture), 'wb') as img:
        img.write(base64.b64decode(image_body))
    return '/static/img/' + picture


def process_commands(all=None, size=None, ne=None, gt=None, gte=None, lt=None, lte=None, **kwargs):
    commands = []
    if kwargs:
        commands.append(kwargs)
    if all:
        commands.append({key: {"$all": value} for key, value in all.items()})
    if size:
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


image_path = to_path(os.path.dirname(get_file_path(__file__)), 'static', 'img')
