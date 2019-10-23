import json

from collections import Counter

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

try:
    from database import mongodb_offline, yesterday
except:
    raise Exception('没有数据库配置文件，无法运行哦')


def index(request):
    return render(request, 'index.html')


@cache_page(60 * 60 * 3)
def api_get_map_data(request):
    province = {}
    word_cloud = []
    db_handler = mongodb_offline.client['新闻(新闻)-offline-cza']
    collections = db_handler.list_collection_names()
    for collection in collections:
        try:
            if collection.startswith('人民政府'):
                doc = db_handler[collection].find_one({'timestamp': int(yesterday.timestamp())})
                province[doc['province']] = doc['count']
                word_cloud.extend(json.loads(doc['jieba_list']))
        except Exception as e:
            print(e)
            continue
    word_cloud_dict = dict(Counter(word_cloud))
    for key in word_cloud_dict:
        if len(str(key).strip()) < 2:
            word_cloud_dict.pop(key)
    return JsonResponse({
        'map_data': [dict(name=name, value=value) for name, value in province.items()],
        'bar': _get_split_bar(max(province.values())),
        'cloud_data': [dict(name=name, value=value) for name, value in word_cloud_dict.items()],
    })


def api_get_china_map_data(request):
    """
    di 应该是定义好的
    然后遍历数据库
    collections = mongodb_offline.client['新闻(新闻)'].list_collection_names()
    try:
        if collection.startswith('人民政府'):
            pass
    [dict(name=name, value=value) for name, value in di.items()]
    """
    province = {}
    word_cloud = []
    db_handler = mongodb_offline.client['新闻(新闻)-offline-cza']
    collections = db_handler.list_collection_names()
    for collection in collections:
        try:
            if collection.startswith('人民政府'):
                doc = db_handler[collection].find_one({'timestamp': int(yesterday.timestamp())})
                province[doc['province']] = doc['count']
                word_cloud.extend(json.loads(doc['jieba_list']))
        except Exception as e:
            print(e)
            continue
    word_cloud_dict = dict(Counter(word_cloud))
    for key in word_cloud_dict:
        if len(str(key).strip()) < 2:
            word_cloud_dict.pop(key)
    return JsonResponse({
        'map_data': [dict(name=name, value=value) for name, value in province.items()],
        'bar': _get_split_bar(max(province.values())),
        'cloud_data': [dict(name=name, value=value) for name, value in word_cloud_dict.items()],
    })

    # return JsonResponse({
    #     'map_data': [
    #         {'name': '北京', 'value': 700},
    #         {'name': '天津', 'value': 300},
    #         {'name': '江西', 'value': 200},
    #         {'name': '吉林', 'value': 100},
    #         {'name': '贵州', 'value': 400},
    #         {'name': '西藏', 'value': 200},
    #         {'name': '香港', 'value': 300},
    #         {'name': '澳门', 'value': 500},
    #     ],
    #
    #     'bar': [
    #         {'start': 500, 'end': 700},
    #         {'start': 300, 'end': 500},
    #         {'start': 200, 'end': 300},
    #         {'start': 0, 'end': 100}
    #     ]
    # })


def api_get_world_cloud_data(request):
    return JsonResponse({
        'cloud_data': [
            {'name': '北京', 'value': 700},
            {'name': '天津', 'value': 300},
            {'name': '江西', 'value': 200},
            {'name': '吉林', 'value': 100},
            {'name': '贵州', 'value': 400},
            {'name': '西藏', 'value': 200},
            {'name': '香港', 'value': 300},
            {'name': '澳门', 'value': 500},
        ]
    })


def _get_split_bar(max_value):
    value = (max_value // 10 + 1) * 10
    four = int(value // 4)
    return [
        {'start': four * 3, 'end': value},
        {'start': four * 2, 'end': four * 3},
        {'start': four, 'end': four * 2},
        {'start': 0, 'end': four}
    ]


if __name__ == '__main__':
    from pprint import pprint

    # pprint(_get_split_bar(123))
    data = Counter([1, 2, 3, 4, 234, 5, 6, 7, 8, 9, 0, 7, 7, 6, 6, ' '])
    print(dict(data))
    for key in dict(data):
        if len(str(key).strip()) < 2:
            data.pop(key)
    print(data)
