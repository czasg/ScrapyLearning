from threading import Thread


def async_by_thread(func):
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=())
        thread.start()
    return wrapper

@async_by_thread
def test1():
    import time
    print('test1...')
    time.sleep(3)
    print('test1-done')

def test2():
    print('test2...')
    print('test2-done')


test1()
test2()
