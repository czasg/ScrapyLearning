import execjs

from czaSpider.czaTools import *

database_path = to_path(get_current_path(__file__), "database")


class AntiJsClearanceMiddleware:
    def __init__(self):
        with open(to_path(database_path, "anti_clearance0_1.js"), encoding='utf-8') as f:
            self.anti_js = execjs.compile(f.read())

    def process_response(self, request, response, spider):
        if re.match("<script>", response.text):
            try:
                cookie = self.anti_js.call("get_cookie", response.text.strip())
                clearance = re.search('__jsl_clearance=(.*)', cookie).group(1)
                return request.replace(cookies={"__jsl_clearance": clearance}, dont_filter=True)
            except:
                return request
        return response
