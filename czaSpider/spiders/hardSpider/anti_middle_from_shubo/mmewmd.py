# 特征 MmEwMD
# FSSBBIl1UgzbN7N443T


# step2 版本检测 return 11   可修正
# _$EI = _$EI.replace(/var _\$.{2}=3,[^;]+;/g, 'return 11;')
# 加上window的一些东西
# clearInterval问题 已修正
# step1 eval 可修正
# [225, 79, 164, 115]存在一处报错 # 可能本来不是问题

# var前面如果时}要加;
# 删除r=m的script
# 作用域问题= =
# 警惕 可能有FSSBBIl1UgzbN7N443T验证

import logging
import re

import execjs
import requests
from scrapy.exceptions import IgnoreRequest

# JS_CACHE_KEY = "spider:js_cache"


# def js_cache(url, **kwargs):
#     js = get_local_redis().hget(JS_CACHE_KEY, url)
#     if not js:
#         js = requests.get(url, **kwargs).text
#         get_local_redis().hset(JS_CACHE_KEY, url, js)
#     return js


# noinspection PyPep8Naming
class MmewmdMiddleWare:
    def process_response(self, request, response, spider):
        if '技术支持：' in response.text:
            return response
        if "9DhefwqGPrzGxEp9hPaoag" not in response.text:
            return response
        if request.dont_filter:
            logging.error("js反爬没有绕过")
            raise IgnoreRequest
        ua = (request.headers[b'User-Agent']).decode()
        cookies = b";".join([i for i in [request.headers.get("Cookie"),
                                         response.headers.get("Set-Cookie")] if i]).decode()
        meta_content = response.xpath('//meta[@id="9DhefwqGPrzGxEp9hPaoag"]/@content').get()
        scripts = "\n".join([i for i in response.xpath('//script/text()').extract()])
        script_src = response.xpath("//script/@src").get()
        # scripts = js_cache(response.urljoin(script_src), headers={"User-Agent": ua}, verify=False) + "\n" + scripts
        append_str = "\\1"
        append_str += "\\2=\\2.replace(/var _.{3}=3,[^;]+;/g, \"return 11;\");"
        # 用来改检查浏览器版本号
        scripts = re.sub("(if\(_\$.{2}\[_\$.{2}\(\)]\){_\$.{2}=_\$.{2}\[_\$.{2}\(\)]\((_\$.{2})\);}else{)",
                         append_str, scripts)

        prefix = """
            window = global;
            meta_element = {
                content: "%s",
                parentNode: {
                    removeChild: function (x) { },
                }
            }
            addEventListener = function (a, b) { };
            document = {
                getElementById: function (id) {
                                return meta_element;
                },
                cookie : "%s",
                documentElement:{
                style: {},
                },
                addEventListener: addEventListener,
                getElementsByTagName: function(name){
                //console.log("getElementsByTagName", name);
                var tag_o=new Object;
                tag_o.getAttribute=function(r){
                //console.log("getAttribute", r)
                };
                var o_parent=new Object;
                tag_o.parentNode=o_parent;
                o_parent.removeChild=function(){};

                var new_array_output = Array();
                new_array_output.push(tag_o);
                //console.log("tag_o", new_array_output);
                return new_array_output;},
                write:function(s){
                //console.log("document.write", s);
                document_write_holder.push(s);
                },

            }
            top = {
                location:{
                href :"%s",
                }
            }

            document_write_holder = [];


            location = top.location;
            navigator = {
                language: "zh-CN",
                userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
                mimeTypes:{},
            };

            screen = {
                width:1920,
                height:1080,
                pixelDepth:24,
                colorDepth:24,
            };

            setInterval = function (func, inter) {
                //console.log("setInterval", func, inter)
            };

            clearInterval = function(){};
            """ % (meta_content.replace("\\", "\\\\"), cookies, response.url)

        final_js = (prefix
                    + "function ppppp(){      %s};"
                      "window.eval(ppppp.toString().slice(20,-1));" % scripts  # 为了eval的作用域的骚操作
                    )
        final_js += "function ccc(){return {cookie:document.cookie}};"
        ret = execjs.compile(final_js).call("ccc")
        cookies = ret["cookie"]
        new_cookie = dict(re.findall("([^=,;\s]+)=([^=,;]+)", cookies))
        new_cookie = {k: v for k, v in new_cookie.items() if k.lower() not in ["max-age", "path", "expires"]}
        return request.replace(cookies=new_cookie, dont_filter=True)
