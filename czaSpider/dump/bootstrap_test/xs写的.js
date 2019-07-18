

// $("#iframe1").height($(window).height() - 40)



$(".isLoginBox").mouseleave(function (e) {
    $(".isloginOut").hide();
});

$(".isLoginBox div").mouseover(function (event) {
    event.stopPropagation();
    $(".isLoginBox div").css({ "background-color": "#7586e4" });
    $(this).css({ "background-color": "#4A61E2" });
});

$(".isLoginBox").mouseover(function () {
    $(".isloginOut").show();
});

$(".goIndex").click(function () {
    window.location.href = "/index.html";
})
$("body").click(function () {
    $(".loginBoxCard").hide();
})

$(".PingTimeout").click(function () {
    // window.sessionStorage.setItem("nows", window.location.href)
    window.location.href = "/set/loginty.html";
});

var nick_name;
$(".img-circle").attr("src", "../images/首页/我的.svg");


var username = window.sessionStorage.getItem("username");
var data_img = window.sessionStorage.getItem("data_img");
var nick_name = window.sessionStorage.getItem("nick_name");
// console.log(username && data_img)
if (username && data_img) {
    $(".img-circle").attr("src", data_img);
    $(".username").text(nick_name);
    $(".username").attr({title:nick_name});
    $(".img-circle").attr("src", window.sessionStorage.getItem("data_img"));
    $(".PingTimeout").hide();
    $(".isLoginBox").show();
} else {
    $(".PingTimeout").show();
    $(".isLoginBox").hide();
}
// islogin();

// 退出登录
$(".isloginOut .goOut").on("click", function () {
    $.ajax({
        type: "get",
        url: componemt + '/logout_api',
        cache: true,
        data: {},
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        success: function (data) {
            data = JSON.parse(data);
            if (data.success == 403) {
                return;
            };
            // console.log(data)
            if (data.success == 200) {
                sessionStorage.clear()
                $(".PingTimeout").show();
                $(".isLoginBox").hide();
                location.reload();
            }
        },
        error: function () {
            Vue.prototype.$message({
                type: 'error',
                message: '退出失败'
            });
        }
    })
});

// 判断是否登录
function islogin() {
    return new Promise((resolve, reject) => {
        $.ajax({
            type: "get",
            url: componemt + '/user/basic',
            cache: true,
            xhrFields: {
                withCredentials: true
            },
            crossDomain: true,
            data: {},
            success: function (data) {
                var res = JSON.parse(data);
                if (res.success == 200) {
                    var username = res.info["用户名称"];
                    var data_img = res.info["头像"];
                    var nick_name = res.info["昵称"];
                    if (username == undefined) {
                        window.sessionStorage.setItem("username", null);
                    } else {
                        window.sessionStorage.setItem("username", username);
                        window.sessionStorage.setItem("data_img", data_img)
                        window.sessionStorage.setItem("nick_name", nick_name)
                    }
                    bind_s();
                    resolve(true);
                } else if (res.success == 403) {
                    window.sessionStorage.setItem("username", null);
                    $(".PingTimeout").show();
                    $(".isLoginBox").hide();
                    Vue.prototype.$notify({
                        title: '警告',
                        message: '当前状态未登录，请及时登录！',
                        type: 'warning'
                    });
                    resolve(false);
                } else {
                    window.sessionStorage.setItem("username", null);
                    resolve(false);
                }
            },
            error: function () {
                resolve(false)
            }
        })
    })

}

function bind_s() {
    username = window.sessionStorage.getItem("username");
    data_img = window.sessionStorage.getItem("data_img");
    nick_name = window.sessionStorage.getItem("nick_name");
    // console.log(username && data_img)
    if (username && data_img) {
        $(".img-circle").attr("src", data_img);
        $(".username").text(nick_name);
        $(".username").attr({title:nick_name});
        $(".isLoginBox .username").text(nick_name);
        $(".img-circle").attr("src", window.sessionStorage.getItem("data_img"));
        $(".PingTimeout").hide();
        $(".isLoginBox").show();
    } else {
        $(".PingTimeout").show();
        $(".isLoginBox").hide();
    }
}

// 去重
function unique1(array) {
    var n = []; //一个新的临时数组
    //遍历当前数组
    for (var i = 0; i < array.length; i++) {
        //如果当前数组的第i已经保存进了临时数组，那么跳过，
        //否则把当前项push到临时数组里面
        if (n.indexOf(array[i]) == -1) n.push(array[i]);
    }
    return n;
}



// 获取返回修改条数
function get_fhxg(username) {
    $.ajax({
        type: "get",
        url: componemt + '/tools/count',
        cache: true,
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        data: {

        },
        success: function (data) {
            // $(".loadingimg").hide();
            var res = JSON.parse(data);
            if (res.success == 403) {
                window.sessionStorage.setItem("username", null);
                return;
            };
            // console.log(res);
            if (res.info["其他"] != 0) {
                $('.continuedpage').show();
                $(".other_num").text(res.info["其他"])
                $('.other_num').show();
            } else {
                $('.continuedpage').hide();
                $('.other_num').text('');
                $('.other_num').hide();
            }

            if (res.info["博客"] != 0) {
                $('.listplayers').show();
                $(".blogs_num").text(res.info["博客"])
                $('.blogs_num').show();
            } else {
                $('.listplayers').hide();
                $('.blogs_num').text('');
                $('.blogs_num').hide();
            }

            if (res.info["诚信数据"] != 0 ||
                res.info["法律"] != 0 ||
                res.info["新闻"] != 0 ||
                res.info["钢铁"] != 0 ||
                res.info["航运"] != 0 ||
                res.info["政府网站"] != 0 ||
                res.info["零碎任务"] != 0) {
                $('.manufacturingShop').show();
            } else {
                $('.manufacturingShop').hide();
            }

            if (res.info["诚信数据"] != 0) {
                $(".fhxg_num").text(res.info["诚信数据"])
                $(".fhxg_num").show();
            } else {
                $(".fhxg_num").text('')
                $(".fhxg_num").hide();
            }

            if (res.info["法律"] != 0) {
                $(".law_num").text(res.info["法律"])
                $(".law_num").show();
            } else {
                $(".law_num").text('');
                $(".law_num").hide();
            }

            if (res.info["新闻"] != 0) {
                $(".news_num").text(res.info["新闻"])
                $(".news_num").show();
            } else {
                $(".news_num").text('')
                $(".news_num").hide();
            }

            if (res.info["钢铁"] != 0) {
                $(".steel_num").text(res.info["钢铁"])
                $(".steel_num").show();
            } else {
                $(".steel_num").text('')
                $(".steel_num").hide();
            }

            if (res.info["航运"] != 0) {
                $(".shipping_num").text(res.info["航运"])
                $(".shipping_num").show();
            } else {
                $(".shipping_num").text('')
                $(".shipping_num").hide();
            }

            if (res.info["政府网站"] != 0) {
                $(".gov_num").text(res.info["政府网站"])
                $(".gov_num").show();
            } else {
                $(".gov_num").text('')
                $(".gov_num").hide();
            }

            if (res.info["零碎任务"] != 0) {
                $(".candy_num").text(res.info["零碎任务"])
                $(".candy_num").show();
            } else {
                $(".candy_num").text('')
                $(".candy_num").hide();
            }


            //
            //
            //
            //
            //
            //
            //
            //
            //

        },
        error: function () { }
    });

}


// $(".contentBody").width($(window).width() - 230);
// $(".contentBody").height($(window).height() - 60);
// window.onresize = function () {
// $(".contentBody").width($(window).width() - 230);
// $(".contentBody").height($(window).height() - 60);
// }

if (window.sessionStorage.getItem("username")) {
    get_fhxg(window.sessionStorage.getItem("username"));
}