import re
import execjs
import traceback
import requests


def _get_clearance(script, url):
    js2 = """
                function getCmd() {
                while (z++) {
                        o = y.replace(/\\b\w+\\b/g, function (y) { return x[f(y, z) - 1] || ("_" + y) });
                        if (o.startsWith("var")){return o;}
                    }
                }
                """
    js0 = re.search("<script>(.*)while\(z\+\+\)try{", script)
    if not js0:
        raise ValueError("原始js格式不正确")
    js0 = js0.group(1)
    s1 = execjs.compile(js0 + js2).call("getCmd")
    print(s1)
    s1 = re.sub(".*document\.cookie=('__jsl_clearance=[\d.|]+'\+.+)\+';Expires=.*", "\\1", s1)
    s1 = re.sub("(var \S+?=)document\.createElement.+firstChild\.href", "\\1'" + url + "'", s1)
    s1 = s1.replace("window.headless", "undefined")
    s1 = s1.replace("window", "[]")
    s1 = execjs.compile("function gets1(){return %s}" % s1).call("gets1")
    key, value = s1.split("=", 1)
    if key == "__jsl_clearance":
        return {key: value}
    raise ValueError("没有计算得到正确的cookie")


def get__jsl_clearance(session):
    url = 'http://www.gsxt.gov.cn/corp-query-homepage.html'
    text = session.get(url).text
    if text.startswith("<script>"):
        try:
            url = re.search("(https?://[^/]+/)", url).group(1)
            clearance = _get_clearance(text, url)
        except:
            raise Exception("计算__jsl_clearance时出错\n" +
                            "------------------------\n" +
                            text +
                            "\n------------------------\n" +
                            traceback.format_exc())
        if clearance:
            return clearance


def get_chuangyu_pic(url):
    with requests.Session() as session:
        return session.get(url, cookies=get__jsl_clearance(session)).content


url = 'http://www.gsxt.gov.cn/cdn-cgi/captcha/bk1j49/4000'
print(get_chuangyu_pic(url))
