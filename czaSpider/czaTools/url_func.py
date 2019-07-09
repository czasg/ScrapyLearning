import re
import json

from czaSpider.czaTools.process_dict import strJoin, arrayJoin

"""
get_next_page: turn the page in a specific format rule
"""


def get_next_page(url=None, format=None, jump=None, diff="_", step=1, check_current_page=None,
                  json_data=None, **kwargs):
    def next_page(steps):
        if isinstance(steps, str):
            steps = int(steps) + step
            print("当前第%d页" % steps)
            return steps
        elif isinstance(steps, int):
            print("当前第%d页" % steps)
            return steps

    url = _json_data(json_data) if json_data else url
    url = _check_current_page(url, format, check_current_page) if check_current_page else url

    if not format:
        print("{url} 无跳转样式，返回当前页".format(url=url))
        return url

    if json_data and "=" in format:
        format = arrayJoin(format.split("="), func=lambda string: '\"%s\"' % string,
                           sepJ=":", strict=True)

    if jump is None:
        reRule = format.replace("%d", "(\d+)")
        return re.sub(reRule, lambda v: format % next_page(v.group(1)), url)
    # reRule = re.sub(diff + "%d", "(?:" + diff + "(\d+))?", format)
    reRule = format.replace(diff + "%d", "(?:" + diff + "(\d+))?")
    return re.sub(reRule, lambda v: format % next_page(v.group(1) or jump), url)


def _check_current_page(url, format, check_next_page):
    if re.search(format.replace("%d", "(\d+)?"), url):
        return url
    return "".join((url, check_next_page))


def _json_data(url):
    return strJoin(json.dumps(url))


if __name__ == "__main__":
    url = 'http://sz.ziroom.com/z/nl/z3-d23008679-b612400051.html'
    for i in range(2):
        url = get_next_page(url, format="p=%d", check_current_page="?p=1")
        print(url)
    form = {
        'test': 'hello',
        'page': '1'
    }
    print(json.loads(get_next_page(json_data=form, format="page=%d")))
    url = "http://xxgk.beihai.gov.cn/bhshjbhj/xzzfzl_84504/index.html"
    print(get_next_page(url, format="index_%d", jump=1))
