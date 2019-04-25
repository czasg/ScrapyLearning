import re

"""
get_next_page: turn the page in a specific format rule
"""


def get_next_page(url, format=None, jump=None, diff="_", step=1, check_current_page=None, **kwargs):
    def next_page(steps):
        if isinstance(steps, str):
            steps = int(steps) + step
            print("当前第%d页" % steps)
            return steps
        elif isinstance(steps, int):
            print("当前第%d页" % steps)
            return steps

    url = _check_current_page(url, format, check_current_page) if check_current_page else url
    if not format:
        print("{url} 无跳转样式，返回当前页".format(url=url))
        return url

    if jump is None:
        reRule = format.replace("%d", "(\d+)")
        return re.sub(reRule, lambda v: format % next_page(v.group(1)), url)
    reRule = re.sub(diff + "%d", "(?:" + diff + "(\d+))?", format)
    return re.sub(reRule, lambda v: format % next_page(v.group(1) or jump), url)


def _check_current_page(url, format, check_next_page):
    if re.search(format.replace("%d", "(\d+)?"), url):
        return url
    return "".join((url, check_next_page))


if __name__ == "__main__":
    url = 'http://sz.ziroom.com/z/nl/z3-d23008679-b612400051.html'
    for i in range(10):
        url = get_next_page(url, format="p=%d", check_current_page="?p=1")
        print(url)
