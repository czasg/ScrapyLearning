from collections import Counter
from django.shortcuts import render
from django.http import JsonResponse, Http404

from mini import miniCache

try:
    from database import *
except:
    raise Exception('没有数据库配置文件，无法运行哦')


def index(request):
    return render(request, 'index.html')


@miniCache(60 * 60 * 3)
def api_get_map_data(request):
    now = get_now_datetime()
    today = get_today_datetime(now)
    if now.hour < 12:
        query_day = get_yesterday_datetime(today)
    else:
        query_day = today
    executor.submit(get_collection_statistical, *('新闻(新闻)', '人民政府', ['标题'], today))
    province = {}
    word_cloud = []
    normal_spider_list = []
    abnormal_spider_list = []
    db_handler = mongodb_offline.client['新闻(新闻)-offline-cza']
    collections = db_handler.list_collection_names()
    for collection in collections:
        try:
            if collection.startswith('人民政府'):
                # if collection.endswith('0000'):
                doc = db_handler[collection].find_one({'timestamp': int(query_day.timestamp())})
                province[doc['province']] = province.get(doc['province'], 0) + doc['count']
                if doc['count']:
                    normal_spider_list.append((collection, doc['count']))
                else:
                    abnormal_spider_list.append((collection, doc['abnormal']))
                word_cloud.extend(json.loads(doc['jieba_list']))
        except Exception as e:
            print(e)
            continue
    return JsonResponse({
        'map_data': [dict(name=name, value=value) for name, value in province.items()],
        'bar': _get_split_bar(max(province.values())),
        'cloud_data': [dict(name=name, value=value)
                       for name, value in Counter(word_cloud).items()
                       if len(name.strip()) > 1],
        'normal_spider_list': sorted(normal_spider_list, key=lambda x: x[1], reverse=True),
        'abnormal_spider_list': sorted(abnormal_spider_list, key=lambda x: x[1], reverse=True),
        'current_day': RE_SEARCH_DAY(str(query_day)).group(1),
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


@miniCache(60 * 60 * 3)
def api_get_map_data_v1(request):
    get_day = int(request.GET.get('day', 0))
    if not get_day:
        return Http404()
    query_day = datetime.fromtimestamp(get_day)
    province = {}
    normal_spider_list = []
    abnormal_spider_list = []
    result, all_jieba_list = get_collection_statistical('新闻(新闻)', '人民政府', ['标题'], query_day, False, False)
    for collection, doc in result.items():
        province[doc['province']] = province.get(doc['province'], 0) + doc['count']
        if doc['count']:
            normal_spider_list.append((collection, doc['count']))
        else:
            abnormal_spider_list.append((collection, doc['count']))
    return JsonResponse({
        'map_data': [dict(name=name, value=value) for name, value in province.items()],
        'bar': _get_split_bar(max(province.values())),
        'cloud_data': [dict(name=name, value=value)
                       for name, value in Counter(all_jieba_list).items()
                       if len(name.strip()) > 1],
        'normal_spider_list': sorted(normal_spider_list, key=lambda x: x[1], reverse=True),
        'abnormal_spider_list': sorted(abnormal_spider_list, key=lambda x: x[1], reverse=True),
        'current_day': RE_SEARCH_DAY(str(query_day)).group(1),
    })

if __name__ == '__main__':
    print(datetime.fromtimestamp(1571673600))
"""
var timeStamp = new Date(new Date().setHours(0, 0, 0, 0)) / 1000
86400
//小时,分钟，秒，毫
//凌晨2点50分50秒0毫秒
now.setHours(02, 50, 50, 0);
"""
