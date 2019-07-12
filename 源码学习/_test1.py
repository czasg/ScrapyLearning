import signal
from pydispatch import dispatcher
from _test import *

if __name__ == '__main__':
    started = object()
    stopped = object()
    signal_test(started, stopped)
    dispatcher.send(signal=stopped)  # 卧槽，这个模块也太好用了把