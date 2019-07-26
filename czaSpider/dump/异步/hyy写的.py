import aiohttp
import asyncio
from lxml import etree
from urllib import parse

url1 = 'http://blog.jobbole.com/all-posts/page/{}/'
url = [url1.format(i) for i in range(1, 11)]
base_url = "http://blog.jobbole.com"
sem = asyncio.Semaphore(10) # 信号量，控制协程数，防止爬的过快


async def get_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.request('GET', url) as resp:
            print(resp.status)
            data = await resp.text()
            return data


def parse_html(data):
    urls = []
    html = etree.HTML(data)
    lis = html.xpath("//*[@id='archive']/div")[:-1]
    for i in lis:
        try:
            href = i.xpath(".//div[2]/p/a[1]/@href")[0]
        except:
            continue
        a = parse.urljoin(base_url, href)
        urls.append(a)
    return urls


async def urls(url):
    data = await get_url(url)
    urls = parse_html(data)
    await request_url(urls)

# 时间为 21.144105672836304
async def request_url(urls):
    while True:
        with(await sem):
            async with aiohttp.ClientSession() as session:
                if len(urls) == 0:
                    break
                i = urls.pop()
                try:
                    async with session.request('GET', i) as resp:
                        data = await resp.text()
                        html = etree.HTML(data)
                        title = html.xpath("//*[@class='entry-header']/h1/text()")
                        print(title[0])
                except Exception as e:
                    print(e)

# print("".join(title).strip())

if __name__ == '__main__':
    import time
    start_t = time.time()
    loop = asyncio.get_event_loop()
    tasks = [urls(url3) for url3 in url]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    print("时间为", time.time()-start_t)