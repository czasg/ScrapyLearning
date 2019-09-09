__file__ = 'sql'

"""User
id：         用户唯一id
email：      用户邮件，注册是使用
passwd：     用户密码。登录使用
admin：      判断用户是否拥有管理员权限
name：       用户姓名
image：      用户头像
create_at：  用户创建时间。创建后不可修改。
"""

"""Blog
id：         博客唯一id
user_id：    博客对应的用户者
user_name：  这个需不需要啊==
user_image： 这个肯定是不需要的 ==
name：       博客标题
summary：    博客摘要
content：    博客内容
create_at：  博客创建时间
count：      博客浏览次数
update_at：  博客更新时间
blog_type：  博客标签分类，这里应该保存未json格式，内容为对应的标签类型，也就是对应的数字
"""