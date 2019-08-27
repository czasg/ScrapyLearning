import requests
import threading


def timeout(func=None, timeout=1):
    def _wrapper(func):
        def wrapper():
            result = []

            def _callback(func):
                result.append(func())

            thread = threading.Thread(target=func)
            thread.setDaemon(True)
            thread.start()
            thread.join(timeout)

            return

        return wrapper

    if func:
        return _wrapper(func)
    return _wrapper


@timeout
def test():
    import time
    print('starting...')
    time.sleep(3)
    print('done')


if __name__ == '__main__':
    test()
