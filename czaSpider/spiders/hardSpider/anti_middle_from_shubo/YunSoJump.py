"""
< !DOCTYPE html > <html xmlns = "http://www.w3.org/1999/xhtml" > <head > <meta http - equiv = "Content-Type"content = "text/html; charset=UTF-8" / ><meta http - equiv = "Cache-Control"content = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0" / ><meta http - equiv = "Connection"content = "Close" / ><script type = "text/javascript" >
function stringToHex(str) {
    var val = "";
    for (var i = 0; i < str.length; i++) {
        if (val == "") val = str.charCodeAt(i).toString(16);
        else val += str.charCodeAt(i).toString(16);
    }
    return val;
}
function YunSuoAutoJump() {
    var width = screen.width;
    var height = screen.height;
    var screendate = width + "," + height;
    var curlocation = window.location.href;
    if ( - 1 == curlocation.indexOf("security_verify_")) {
        document.cookie = "srcurl=" + stringToHex(window.location.href) + ";path=/;";
    }
    self.location = "/zwdt/bzdt.htm?security_verify_data=" + stringToHex(screendate);
}
< /script>

<script>
setTimeout("YunSuoAutoJump()", 50);
</script >
</head>
<!--2019-08-28 14:19:11--></html >

"""

# 特征 YunSuoAutoJump()
suffix = "security_verify_data=313932302c31303830"


def stringToHex(s):
    return "".join([hex(ord(i))[2:] for i in s])


class YunSuoAutoJumpDevilMiddleWare:
    def process_response(self, request, response, spider):
        text = response.text
        url = request.url
        if "YunSuoAutoJump" in text:
            if "screendate" in text:
                url = url + ("&" if "?" in url else "?") + suffix
                return request.replace(url=url, cookies={"srcurl": stringToHex(url)})
            url = url.replace(("&" if "&" in url else "?") + suffix, "")
            return request.replace(url=url, dont_filter=True)
        return response
