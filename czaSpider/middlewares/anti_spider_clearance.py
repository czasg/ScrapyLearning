import execjs
import re

def get_anti_spider_clearance(js_string):
    script_content = """
var window = {
 headless: NaN
}
var get_cookie = function(js_code) {
    var re = /var.*?pop\(\)\);/
    args = re.exec(js_code)[0]
    eval(args)

	var func = function(z){
	    var aim = y.replace(/\b\w+\b/g,function(y) {
            return x[f(y, z) - 1] || ("_" + y)
	    })
	    return aim;
	};

    while (1){
        aim = func(z)
        if (aim.indexOf("document.cookie") != -1){
            doc = aim;
            break
        }else{
            z += 1
        }
    }
    return doc;
    var re = /document.cookie='(.*?)\+';Expires/
    cookie = re.exec(doc)[1]

    var re = /.*?'\+(.*)/;
    key = re.exec(cookie)[1]
    cookie = cookie.replace("'\+" + key, eval(key))
    return cookie
}
"""
    anti_js = execjs.compile(script_content)
    cookie = anti_js.call("get_cookie", js_string.strip())
    return cookie


if __name__ == '__main__':
    import requests
    # pic_url = 'http://www.gsxt.gov.cn/cdn-cgi/captcha/bk1j49/1'
    url = 'http://www.gsxt.gov.cn/corp-query-homepage.html'
    with requests.Session() as session:
        text = session.get(url).text
        js_code = re.search('(<script.*</script>)', text).group(1)
        print(js_code)
        print(get_anti_spider_clearance(js_code))

"""
< script >
var x = "@36@D@@__jsl_clearance@@for@createElement@Tue@@@@try@v@zYMC@AC@join@function@z@@JgSe0upZ@@GMT@toString@e@1500@1572939341@@@location@@@@else@@return@@search@0@08@53@split@@fromCharCode@@cookie@@@false@A@@Path@@String@Array@charCodeAt@charAt@@f@@substr@KL@pathname@toLowerCase@firstChild@1@challenge@g@DOMContentLoaded@window@chars@0xFF@@19@@@05@@href@@div@a@U@@@https@addEventListener@2@@length@while@reverse@captcha@attachEvent@onreadystatechange@d@new@document@@Nov@replace@@@@rOm9XFMtA3QKV7nYsPGT4lifyWwkq5vcjH2IdxUoCbhERLaz81DNB6@@41@var@eval@@match@0xEDB88320@@@Expires@if@parseInt@catch@@@8@innerHTML@35@RegExp@@@setTimeout@".replace(/@*$/, "").split("@"),
y = "2a w=i(){2t('u.1u=u.1e+u.C.23(/[\\?|&]1I-1i/,\\'\\')',q);20.K='5=r.F|D|'+(i(){A [({}+[]).18((-~[]|-~-~[]))+(-~-~[]+[[]][D])+(-~-~[]+[[]][D]),'f',({}+[[]][D]).18(([1D]+(+!{})>>1D))+((-~[]<<-~[])+(-~[]<<(-~[]<<-~[]))+[[]][D])+({}+[]).18(-~[])+[((-~-~[]^-~~~[]))/~~!/!/+[]+[[]][D]][D].18(-~~~[]-~![]+([-~![]-~![]]+(+!{})>>-~![]-~![])),'j',[[1D]/~~[]+[[]][D]][D].18((+!{})),'11',[[][{}]+[]][D].18(-~![])+((-~[]<<-~[])+(-~[]<<(-~[]<<-~[]))+[[]][D]),'e',[~~!/!/],'1d',[[][{}]+[]][D].18(-~![])+[-~[]+(-~[]<<-~[])],'g',((1D)*[1D]+[]+[])+((1D)*[1D]+[]+[]),'1y%',[-~[]+(-~[]<<-~[])],'3'].h('')})()+';2h=9, 1s-22-1p E:2p:29 n;13=/;'};2i((i(){d{A !!1l.1C;}2k(p){A 10;}})()){20.1C('1k',w,10)}y{20.1J('1K',w)}",
f = function(x, y) {
    var a = 0,
    b = 0,
    c = 0;
    x = x.split("");
    y = y || 99;
    while ((a = x.shift()) && (b = a.charCodeAt(0) - 77.5)) c = (Math.abs(b) < 13 ? (b + 48.5) : parseInt(a, 36)) + y * c;
    return c
},
z = f(y.match(/\w/g).sort(function(x, y) {
    return f(x) - f(y)
}).pop());
while (z++) try {
    eval(y.replace(/\b\w+\b/g,
    function(y) {
        return x[f(y, z) - 1] || ("_" + y)
    }));
    break
} catch(_) {} < /script>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      /
"""

"""
_2a _w=function(){8('location._1u=location._1e+location.search.onreadystatechange(/[\?|&]length-toLowerCase/,\'\')',1500);reverse.cookie='__jsl_clearance=1572939341.53|0|'+(function(){return [({}+[]).String((-~[]|-~-~[]))+(-~-~[]+[[]][0])+(-~-~[]+[[]][0]),'zYMC',({}+[[]][0]).String(([_1D]+(+!{})>>_1D))+((-~[]<<-~[])+(-~[]<<(-~[]<<-~[]))+[[]][0])+({}+[]).String(-~[])+[((-~-~[]^-~~~[]))/~~!/!/+[]+[[]][0]][0].String(-~~~[]-~![]+([-~![]-~![]]+(+!{})>>-~![]-~![])),'z',[[_1D]/~~[]+[[]][0]][0].String((+!{})),'_11',[[][{}]+[]][0].String(-~![])+((-~[]<<-~[])+(-~[]<<(-~[]<<-~[]))+[[]][0]),'v',[~~!/!/],'f',[[][{}]+[]][0].String(-~![])+[-~[]+(-~[]<<-~[])],'AC',((_1D)*[_1D]+[]+[])+((_1D)*[_1D]+[]+[]),'_1y%',[-~[]+(-~[]<<-~[])],'D'].join('')})()+';eval=Tue, 19-attachEvent-chars 08:parseInt:replace GMT;false=/;'};_2i((function(){try{return !!challenge._1C;}0xEDB88320(e){return cookie;}})()){reverse._1C('1',_w,cookie)}else{reverse.while('reverse',_w)}
"""