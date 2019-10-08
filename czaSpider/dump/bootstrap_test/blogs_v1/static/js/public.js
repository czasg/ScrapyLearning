if (! String.prototype.trim) {
    String.prototype.trim = function() {
        return this.replace(/^\s+|\s+$/g, '');
    };
}

if (! String.prototype.limit) {
    String.prototype.limit = function() {
        return this.replace(/<.*?>/g, '').substring(0, 100);
    };
}

if (! Number.prototype.toDateTime) {
    var replaces = {
        'yyyy': function(dt) {
            return dt.getFullYear().toString();
        },
        'yy': function(dt) {
            return (dt.getFullYear() % 100).toString();
        },
        'MM': function(dt) {
            var m = dt.getMonth() + 1;
            return m < 10 ? '0' + m : m.toString();
        },
        'M': function(dt) {
            var m = dt.getMonth() + 1;
            return m.toString();
        },
        'dd': function(dt) {
            var d = dt.getDate();
            return d < 10 ? '0' + d : d.toString();
        },
        'd': function(dt) {
            var d = dt.getDate();
            return d.toString();
        },
        'hh': function(dt) {
            var h = dt.getHours();
            return h < 10 ? '0' + h : h.toString();
        },
        'h': function(dt) {
            var h = dt.getHours();
            return h.toString();
        },
        'mm': function(dt) {
            var m = dt.getMinutes();
            return m < 10 ? '0' + m : m.toString();
        },
        'm': function(dt) {
            var m = dt.getMinutes();
            return m.toString();
        },
        'ss': function(dt) {
            var s = dt.getSeconds();
            return s < 10 ? '0' + s : s.toString();
        },
        's': function(dt) {
            var s = dt.getSeconds();
            return s.toString();
        },
        'a': function(dt) {
            var h = dt.getHours();
            return h < 12 ? 'AM' : 'PM';
        }
    };
    var token = /([a-zA-Z]+)/;
    Number.prototype.toDateTime = function(format) {
        var fmt = format || 'yyyy-MM-dd hh:mm:ss'
        var dt = new Date(this * 1000);
        var arr = fmt.split(token);
        for (var i=0; i<arr.length; i++) {
            var s = arr[i];
            if (s && s in replaces) {
                arr[i] = replaces[s](dt);
            }
        }
        return arr.join('');
    };
}

function refresh() {
    var
        t = new Date().getTime(),
        url = location.pathname;
    if (location.search) {
        url = url + location.search + '&t=' + t;
    }
    else {
        url = url + '?t=' + t;
    }
    location.assign(url);
}

function redirect(url) {
    var
        hash_pos = url.indexOf('#'),
        query_pos = url.indexOf('?'),
        hash = '';
    if (hash_pos >=0 ) {
        hash = url.substring(hash_pos);
        url = url.substring(0, hash_pos);
    }
    url = url + (query_pos >= 0 ? '&' : '?') + 't=' + new Date().getTime() + hash;
    location.assign(url);
}

function _httpJSON(method, url, data, callback) {
    var opt = {
        type: method,
        dataType: 'json'
    };
    if (method==='GET') {
        opt.url = url + '?' + data;
    }
    if (method==='POST') {
        opt.url = url;
        opt.data = JSON.stringify(data || {});
        opt.contentType = 'application/json';
    }
    $.ajax(opt).done(function (r) {
        if (r && r.error) {
            alert(r.error)
            return
        }
        return callback(r);
    }).fail(function (jqXHR, textStatus) {
        return callback({'error': 'http_bad_response', 'data': '' + jqXHR.status, 'message': '网络好像出问题了 (HTTP ' + jqXHR.status + ')'});
    });
}

function getJSON(url, data, callback) {
    if (arguments.length===2) {
        callback = data;
        data = {};
    }
    if (typeof (data)==='object') {
        var arr = [];
        $.each(data, function (k, v) {
            arr.push(k + '=' + encodeURIComponent(v));
        });
        data = arr.join('&');
    }
    _httpJSON('GET', url, data, callback);
}

function postJSON(url, data, callback) {
    if (arguments.length===2) {
        callback = data;
        data = {};
    }
    _httpJSON('POST', url, data, callback);
}

function gotoTop(min_property, min_height) {
    var toTop_html = '<button id="toTop" class="btn btn-default"">返回顶部</button>';
    $(min_property).append(toTop_html);
    $('#toTop').click(function(){
        $('html,body').animate({scrollTop: 0}, 700);
    }).hover(
        function(){ $(this).addClass("hover"); },
        function(){ $(this).removeClass("hover");
    });
    min_height ? min_height = min_height : min_height = 600;
    $(window).scroll(function(){
        var s = $(window).scrollTop();
        if( s > min_height){
            $("#toTop").fadeIn(100);
        } else {
            $("#toTop").fadeOut(200);
        };
    });
};

function getBlogType(type) {
    if (type === 1) {
        current_type_text = '前端'
    } else if (type === 2) {
        current_type_text = '后端'
    } else if (type === 3) {
        current_type_text = '爬虫'
    } else if (type === 4) {
        current_type_text = '生活'
    } else {
        current_type_text = '未指定分类'
    }
    return current_type_text
}

