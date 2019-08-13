import requests
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(3)

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

def main():
    raw_proxies = ['60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
                   '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
                   '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797',
                   '60.13.42.83:9999', '37.187.127.216:8080', '111.194.108.198:9797']
    for proxy in raw_proxies:
        done = pool.submit(request, proxy)
        done.add_done_callback(read_data)


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