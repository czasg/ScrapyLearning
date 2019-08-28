import logging
import re
import traceback

import execjs
from scrapy.exceptions import IgnoreRequest

logger = logging.getLogger("ClearanceCacuMiddleWare")


class ClearanceCacuMiddleWare:
    @staticmethod
    def get_clearance(script, url):
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

        # 把计算cookie的部分单独提取出来
        s1 = re.sub(".*document\.cookie=('__jsl_clearance=[\d.|]+'\+.+)\+';Expires=.*", "\\1", s1)
        # var _72=document.createElement('div');_72.innerHTML='<a href=\'/\'>_28</a>';_72=_72.firstChild.href;
        # 可以替换为 var _72='http://www.gsxt.gov.cn/'
        s1 = re.sub("(var \S+?=)document\.createElement.+firstChild\.href", "\\1'" + url + "'", s1)
        # 一些影响js运算的对象
        s1 = s1.replace("window.headless", "undefined")
        s1 = s1.replace("window", "[]")
        s1 = execjs.compile("function gets1(){return %s}" % s1).call("gets1")
        key, value = s1.split("=", 1)
        if key == "__jsl_clearance":
            return {key: value}
        raise ValueError("没有计算得到正确的cookie")

    def process_response(self, request, response, spider):
        text = response.text
        if text.startswith("<script>"):
            if request.dont_filter:
                logger.error("clearance重试依然失败")
                raise IgnoreRequest()
            try:
                url = re.search("(https?://[^/]+/)", response.url).group(1)
                clearance = self.get_clearance(text, url)
            except:
                logger.error("计算__jsl_clearance时出错\n" +
                             "------------------------\n" +
                             text +
                             "\n------------------------\n" +
                             traceback.format_exc())
                raise IgnoreRequest()
            if clearance:
                logger.info("计算得到clearance")
                return request.replace(dont_filter=True, cookies=clearance)  # 插入新计算出来的cookie
            logger.error("计算得到clearance，但是输出为空")
            raise IgnoreRequest()

        return response
