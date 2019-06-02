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
	    return aim
	}

    while (1){
        aim = func(z)
        if (aim.indexOf("document.cookie") != -1){
            doc = aim
            break
        }else{
            z += 1
        }
    }

    var re = /document.cookie='(.*?)\+';Expires/
    cookie = re.exec(doc)[1]

    var re = /.*?'\+(.*)/;
    key = re.exec(cookie)[1]
    cookie = cookie.replace("'\+" + key, eval(key))
    return cookie
}


