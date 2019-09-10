ANTI_COOKIE_FIRST = 'anti_spider_first'
ANTI_COOKIE_SECOND = 'anti_spider_second'


def check_anti_spider(anti_cookie):
    return anti_cookie


def stringToHex(s):
    return "".join([hex(ord(i))[2:] for i in s])
