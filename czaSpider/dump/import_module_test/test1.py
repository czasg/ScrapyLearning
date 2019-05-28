import argparse

from importlib import import_module
# import czaSpider.dump.import_module_test.test
"""import module 不能往上找包吗"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="This is Test")
    parser.add_argument("path", help="PATH")
    # parser.add_argument("func", help="FUNC")
    # parser.add_argument("args", nargs='*', help="te")

    allArgs = parser.parse_args()
    path = allArgs.path
    md = import_module(path)
    getattr(md, "hello")()
