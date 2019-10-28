from collections import Counter
from django.shortcuts import render
from django.http import JsonResponse, Http404

from mini import miniCache

try:

    from database import *
    from base_tools import init, multi_table, get_data_first, get_data_second, get_data_third
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
    filter_province = '0000' if request.GET.get('just_choose_province', None) == 'true' else ''
    get_day = int(request.GET.get('day', 0))
    if not get_day:
        return Http404()
    query_day = datetime.fromtimestamp(get_day)
    province = {}
    normal_spider_list = []
    abnormal_spider_list = []
    result, all_jieba_list = get_collection_statistical('新闻(新闻)', '人民政府', ['标题'], query_day, False, False,
                                                        filter_province)
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


@miniCache(60 * 60 * 3)
def api_get_operation_data(request):
    # task_name = request.GET.get('task_name', None)
    # if not task_name or task_name not in multi_table: return Http404()
    # now = get_now_datetime()
    # init(task_name, '{}.01'.format(now.year), version=multi_table[task_name])
    # return JsonResponse({
    #     'data_summary': get_data_first(),
    #     'data_statistical': get_data_second(),
    #     'data_bar': get_data_third(),
    # })
    test = """{"data_summary": [["\u8bda\u4fe1\u6570\u636e\u603b\u8bb0\u5f55", 25229], ["\u8bda\u4fe1\u6570\u636e\u603b\u4efb\u52a1", 843], ["\u8bda\u4fe1\u6570\u636e\u6709\u8fc7\u8fd0\u7ef4\u8bb0\u5f55\u7684\u4efb\u52a1", 796], ["\u8bda\u4fe1\u6570\u636e\u5904\u4e8e\u5e9f\u5f03\u72b6\u6001\u7684\u4efb\u52a1", 333], ["\u8bda\u4fe1\u6570\u636e\u5386\u53f2\u5165\u5e93\u5b8c\u6210\u4efb\u52a1", 724], ["\u5165\u5e93\u4efb\u52a1\u4e2d\u8fd0\u7ef4\u53d1\u73b0\u5f02\u5e38\u7684\u4efb\u52a1", 493, "68%"], ["\u5165\u5e93\u4efb\u52a1\u4e2d\u8fd0\u7ef4\u5e9f\u5f03\u7684\u4efb\u52a1", 258, "35%"]], "data_statistical": [["mean", 2.7459584295612007, 9.930715935334874, "27%"], ["std", 1.9424923299646777, 3.7999517169386405, "-"], ["min", 1.0, 2.0, "-"], ["50%", 2.0, 9.0, "-"], ["max", 15.0, 19.0, "-"]], "data_bar": [["2019\u5e741\u6708", "2019\u5e742\u6708", "2019\u5e743\u6708", "2019\u5e744\u6708", "2019\u5e745\u6708", "2019\u5e746\u6708", "2019\u5e747\u6708", "2019\u5e748\u6708", "2019\u5e749\u6708", "2019\u5e7410\u6708"], [0, 0, 0, 0, 144, 37, 50, 15, 0, 12], [97, 2, 0, 38, 516, 208, 133, 111, 106, 38], [596, 596, 596, 596, 671, 531, 515, 475, 471, 479]]}"""
    test = json.loads(test)
    return JsonResponse(test)
