import os
import re

from czaSpider.czaTools.path_func import get_current_path, to_path


# interface for czaTools project
def get_test_path(filename):
    filename = re.search('.*/(.*)\..*', filename).group(1) if '/' in filename else filename
    setPath = to_path(get_current_path(__file__), filename)
    testSet = os.listdir(setPath)
    res = [to_path(setPath, file) for file in testSet]
    if all([os.path.isfile(file) for file in res]):
        return res
    else:
        raise ValueError("There exist no file in set database")


if __name__ == "__main__":
    get_test_path("img2num")
    print(to_path('cza', 'is'))

