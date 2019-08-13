import requests
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(13)

def request(proxy):
    proxies = proxy and {sch: "{sch}://{proxy}".format(sch=sch, proxy=proxy) for sch in ["http", "https"]}
    try:
        r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
        if r.status_code == 200 and r.json().get("origin"):
            return True
        return False
    except:
        return False

def read_data(future,*args,**kwargs):
    response = future.result()
    print(response)

def valid_useful_proxy_thread(proxy):
    print('11')
    return pool.submit(request, proxy)

def main():
    raw_proxies = ['60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
                   '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
                   '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
                   '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
                   '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
                   '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
                   '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
                   '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
                   '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
                   '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
                   '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
                   '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797']
    count = 0
    for proxy in raw_proxies:
        count += 1
        # done = pool.submit(request, proxy)
        # done.add_done_callback(read_data)
        # done = valid_useful_proxy_thread(proxy)
        # done.add_done_callback(read_data)
        def _callback(future, count=count):
            r = future.result()
            if r:
                print(count, r)
            else:
                print(count, r)

        done = pool.submit(request, proxy)
        done.add_done_callback(_callback)



    # done = pool.submit(request)
    # done.add_done_callback(read_data)

if __name__ == '__main__':
    import time
    now = time.time()
    main()
    pool.shutdown(wait=True)
    # print('using:', int(time.time()-now))

    # raw_proxies = ['60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
    #                '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
    #                '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
    #                '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797']
    # for i in raw_proxies:
    #     print(request(i))
    print('using:', int(time.time() - now))