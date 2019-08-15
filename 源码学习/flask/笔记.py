__file__ = 'note'


"""
app.debug = True  # 调试打开后，代码改动支持自动重启
app.run()  # app.run(debug=True)


@app.route('/user/<username>')  # 通过这种形式，可以获取对应的变量规则
def show_user_profile(username):
@app.route('/post/<int:post_id>')  # 还可以指定输入字段的类型
def show_post(post_id):
# int	接受整数
# float	同 int ，但是接受浮点数
# path	和默认的相似，但也接受斜线


@app.route('/projects/') # 访问一个结尾不带斜线的 URL 会被 Flask 重定向到带斜线的规范 URL 去
@app.route('/about')     # 访问结尾带斜线的 URL 会产生一个 404 “Not Found” 错误。


url_for()  # ????


@app.route('/login', methods=['GET', 'POST'])  # 可以通过这种methods的方法指定请求类型
if request.method == 'POST':


url_for('static', filename='style.css')  # 这种方式生成静态文件???
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):  # 这种可以指定两种路径的url，是个狼人
    return render_template('hello.html', name=name)  # 还是引用JinJa2模板好一点啊


# 表单数据（ POST 或 PUT 请求提交的数据）
request.form['username']  # requests.post(url, data={'info': content})
# URL 中提交的参数 （ ?key=value ）:
request.args.get('q', '')
# 文件上传  确保属性 enctype="multipart/form-data" 
f = request.files['the_file']
f.save('/var/www/uploads/uploaded_file.txt')
# 如果你要把文件按客户端提供的文件名存储在服务器上,  Werkzeug 提供的 secure_filename() 函数
from werkzeug import secure_filename
f.save('/var/www/uploads/' + secure_filename(f.filename))


# Cookies
username = request.cookies.get('username')  # 通过get方式获取Cookie
resp = make_response(render_template(...))  # 通过make_response构造一个返回对象
resp.set_cookie('username', 'the username')
return resp


# 重定向和错误
from flask import abort, redirect, url_for
@app.route('/')
def index():
    return redirect(url_for('login'))  # 这应该是一个重定向的意思，但是这里的url_for... 啥意思???
# 当你访问主页，会从主页重定向到一个不能访问的页面 （401 意味着禁止访问），但是它展示了重定向是如何工作的。
@app.route('/login')
def login():
    abort(401)  # 直接返回在此处就返回了401，后序代码根部不会执行
    this_is_never_executed()
# 当你向返回具体的错误页面信息给用户的时候，可以使用渲染模板的功能，且最后指定一个404，说明此页面是异常的
from flask import render_template

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404



# 关于响应
1 如果返回的是一个合法的响应对象，它会从视图直接返回。
2 如果返回的是一个字符串，响应对象会用字符串数据和默认参数创建。
3 返回的是一个元组 元组必须是 (response, status, headers) 的形式 至少包含一个元素。 status 值会覆盖状态代码， headers 可以是一个列表或字典，作为额外的消息标头值

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404
# 可以简写为
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

"""



