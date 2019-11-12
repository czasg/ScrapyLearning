__FILE__ = "Unfinished Schedule"

# todo
"""
2019.07.16 - 各种后端知识，如缓存、优化之路，太多了，学不完啊都不会啊
2019.07.23 - socket维护分布式队列，
2019.08.17 - mysql数据类型有哪些，什么组电选择什么类型，类型字节大小、限制条件。索引问题。
2019.08.19 - rabbitmq怎么玩啊，各种exchange还有key，晒意思  https://www.cnblogs.com/huanggy/p/9695712.html
2019.08.22 - scrapy如何做持久化数据的保存，有待研究哦
2019.08.27 - 微信爬虫和展示可以提上进程了，对于如何重新架构也可以提上进程了，还是以aiohttp为主，flask和django为辅，进行web开发。前端倒是一个需要好好构造的地方
2019.08.27 - 学习mysql不错的计划教程：https://blog.csdn.net/hw478983/article/details/78813938
2019.08.28 - https://github.com/FanhuaandLuomu 这个人的爬虫确实可以啊
2019.08.28 - https://keras-cn.readthedocs.io/en/latest/  不错的中文学习文档
2019.08.29 - 微信这验证码这玩意要是实在搞不定，可以试试第三方查询网站：https://chuansongme.com/
2019.08.31 - 改版确实非常的有必要。文件服务器耦合太高了，完全离不开了
2019.09.04 - 目前来说验证码的进度已经开始了，但是是否能够识别成功还是一个问题。是在不成功，可以试下去除正铉后或者直接使用比较干净的图片也可以呀
2019.09.06 - Scrapy的指定路径查询，也可以写一个开源项目。但是如何编写爬虫指令呢，这倒是一个问题。协程scrapy-redis那种就差不多了，嘿嘿
2019.09.08 - 好像看到了自由职业的影子了，有很大的难度啊。人脸识别什么的都知识基础了吗 - 这玩意还需要和硬件进行结合，手机app端的相机调用等等，不太好搞啊
2019.10.08 - blog是逐渐的在完善，但是还是差了太多，让人难受，希望可以坚持下去。慢慢来，别慌
2019.10.09 - pip install graphviz 画流程图还挺不错的，很nice很棒
2019.10.15 - 协议好文https://blog.csdn.net/qq_33616529/article/details/78288883
2019.10.17 - python好文 https://docs.python.org/3/reference/datamodel.html
2019.10.17 - asyncio好文 https://docs.python.org/zh-cn/3/library/asyncio-task.html
2019.10.21 - aiohttp好文 https://www.bookstack.cn/read/aiohttp-chinese-documentation/aiohttp%E6%96%87%E6%A1%A3-ClientUsage.md
2019.10.28 - python好文，多看官方文档，看看如何并发执行任务
2019.10.31 - 用pycharm进行打点来学习异步流程
2019.11.03 - https://setuptools.readthedocs.io/en/latest/setuptools.html
2019.11.06 - 极验 滑块 算法优化。写不出来就去抄一个
2019.11.06 - 验证码终究是个大问题，点击和滑块都是。也就是中文识别+数字识别+缺口识别
2019.11.06 - 在tool中可以加入list或者字典的一些骚方法。自己写一个也是极好的
2019.11.07 - 我去，scrapy包中真是有好多好东西呀。可以看着拿呀。比如对url的一些处理，不就又可以增加了嘛
2019.11.08 - 工具中方便解析的还是要好好添加一些呀，比如页面dom解析，table之类的，还有excel或者是word之类的解析。pdf转码的呢，这个是否需要好好写一个
2019.11.08 - https://zh.d2l.ai/chapter_preface/preface.html  学习好文
2019.11.08 - https://github.com/apachecn/AiLearning  超级学习好文
2019.11.12 - 用python手写队列、单向链表，双向链表，二叉树这些。可以作为数据结构那一栏
"""

"""DONE!
2019.11.07 - logging好文 - https://cloud.tencent.com/developer/section/1369390
2019.11.06 - logging - 模块也需要加一个
2019.11.07 - 邮件模块也可以加进来，不错不错
2019.10.16 - 回去把简书的文章写好吧，github上面的readme也要好好写下，总感觉不太对，别人看不懂就很尴尬
2019.08.20 - css动态图https://www.jianshu.com/p/3a0fb1e30ec5     https://www.zhangxinxu.com/wordpress/2010/11/css3-transitions-transforms-animation-introduction/
2019.10.08 - 今天还算不错。框架子基本上是搭建出来了。明天把相关数据给填进去就差不多了。这里会设计到后端的接口，有点烦人。
2019.09.30 - https://blog.csdn.net/cc7756789w/article/details/45974301项目发布的方法，或许会用到呢
2019.10.13 - pyws测试要进行了呀，可以先把项目提交进去再说。看看那这个该怎么高。
2019.10.13 - 测试内容主要四个。自动回复内容。点对点回复内容。点对多回复内容。广播轮询。 
2019.10.15 - 还需要测试在linux环境下是否可以测试成功，然后试下python3.5是否有问题==，不排除这个可能
2019.10.15 - 还需要测试下是否智能传递字符串，如何传递二进制会怎么样呢
2019.09.09 - 规划好2019终极计划
2019.09.09 - 微信接口有一个itchat，感觉不错，很多人再用
2019.10.08 - blog页面-右边的玩意，最新的评论+分类汇总+关于本站的链接（里面放一些自己的qq微信微博之类的，下面是文章汇总，留言汇总，紧接着是最新留言。然后是分类汇总+再接着就是阅读最多的文章前三，）
2019.09.28 - 前端使用Vue汇总一个总的绘图函数，然后加入滚动监听，感觉可以的。聊天那玩意也是一个坑
2019.09.16 - socket使用socketserver这个原生库，然后加入websocket的解析，然后使用数据局对用户的访问进行保存与读取，目前暂定redis和mongodb，这两个在同一个线程里面会不会有有危险啊
             用户名就使用雪花算法的id，mongodb库名和redis名字都想一下就行，插入什么的应该都不是问题。
2019.08.29 - 自己的人物画像，这个感觉比简历调一些哦~这玩意咋实现啊。这玩意首先要接入github的接口，感觉不太简单。但是过去的数据是可以存到自己的数据库的，这个是没有问题的，只不过需要更新把。
2019.08.14 - import socketserver / from http.server import HTTPServer, BaseHTTPRequestHandler 这来年各个有点神奇的库，应该可以直接处理socket
2019.09.10 - 今天要是能把新blog装好，也算是功德无限把
2019.09.11 - 图片降噪算法需要好好找一下
2019.09.11 - 反爬是不是需要重新再起一个服务，类似裁判文书网这样的
2019.09.09 - 加入第二道反爬机制，YunSuoAutoJump
2019.08.13 - 可以搭建聊天的系统吗，这个好像超级掉的样子
2019.07.20 - 理下最近思路。爬虫：就是scrapy框架问题。后端：Django源码尝试看看。前端：特效部分不谈，太坑了。
2019.07.14 - 逐渐构造散乱的知识点，是否可以联合起来（bootstrap、Vue、js、css、eCharts），进行一次自我突破?????主要是前端知识，后端也很多都是零散的知识点
2019.07.29 - Scrapy系列教程应该出了。模仿源码：基本的Request或Response对象管理|实现异步下载|加入引擎管理|加入调度器管理|加入下载器管理|
2019.08.13 - Scrapy中间件写的太少了，没有感觉，体会不到精髓
2019.08.13 - self.stats.inc_value(key) - 这行代码有点眼熟啊，这是干啥作用的呢
2019.09.04 - 目前等验证码实现，就可以开始着手进行改版了。改版首先需要将后台进行一次整理，按照以前的方法即可，将对应的板块放在一起
2019.09.04 - 前端大改版，清除多余的测试代码，要开始着手写一写大方法了，和xs一样就好了，难啊
2019.09.04 - 可以开始练习30天js了和css了。搞完就开始整改！
2019.07.28 - 技能Http协议，还有数据库，我的天呢，都是坑，还多不知道，面试咋搞啊
2019.08.01 - blog注册页似乎有点问题，那个点
2019.08.12 - Mongodb的位算法是什么意思，位算法，感觉本来就很扯淡的样子
2019.07.31 - 廖雪峰老师的java，有点掉啊
2019.07.19 - 能不能在数据统计图中加入像xs写的那样的数据过滤功能，感觉很不错的样子
2019.07.19 - Scrapy虽然说最基本的流程走通了，但是还有很多细节处理没有抓到，他的通用中间件是如何工作的，等等
2019.07.03 - aiohttp中部分源码，还是可以了解下
2019.07.14 - 从新定义新目标，Scrapy源码需要尽快拿下，之后还有Django源码解析。这个又是一个巨无霸，哎，何时是个头
2019.07.15 - 杨辉三角，找盘子问题，求素数。codepen  --- atom   前端不错的编辑器
2019.07.22 - KNN整理下
2019.09.02 - github的接口其实是一个爬虫，不需要实时的取统计把，获取某一天的数据，然后存入数据库。mongo库就可以。可以试试 - github的接口需要实现一个了，在实现之后可以开始着手重构了，后端其实重构的不是很多，主要是html页面需要重构，这个确实麻烦
2019.09.02 - github查询提交次数的基础功能实现了，还不错
2019.08.29 - 第三方IP代理池维护，接口可以实现了，后台都挂一起把，实在压力大可以在挂在老胡那边。这玩意毕竟还是自己需要使用的啊
2019.08.29 - (废弃，意义基本没有)（各个区域的不一样，需要爬取各个市级的接口，感觉nice呀）计算随后薪水的接口实现一个，放在网页上，这个还是可以的。不错哦！这玩意还怎么用爬虫啊，这就很nice了啊
2019.08.29 - pdf转码接口，我觉得，真的也可以实现一个啊，但是转码服务挂在那呢，这倒是一个问题啊。囧
2019.08.30 - 自如房价的问题，这玩意我现在测试失败，但是从线上的角度看居然是对的，不太可思议啊，怎么回事
2019.08.31 - ocr识别接口可以移植过来，感觉不错的样子哦
2019.08.18 - flask部署，参考官方文档http://www.pythondoc.com/flask/deploying/  ，或者这货的似乎也不错https://www.cnblogs.com/xmxj0707/p/8452881.html
             command=gunicorn -c gunc.py hello:app    ; supervisor启动命令
             supervisord -c supervisor.conf
             supervisorctl reload :修改完配置文件后重新启动supervisor
2019.08.02 - 周末应该干点啥：
             scrapy爬虫的流程，要自觉点搞出来，只要把这个搞出来了，那干啥基本都好说。
             Django的官方文档，还没有吃完，只吃了一点点啊，这个还需要努力一把
             Java代码，这个有必要看吗，可以尝试性看下吧，毕竟还是主看python
             文书网那反爬咋搞啊
2019.07.29 - scrapy什么时候发送各种信号，signal.spider_open，有几种，分别什么时候发送，这个应该了解下
2019.07.18 - 反爬哪里似乎有点bug，误操可能导致无限回调??????
2019.08.14 - 现在问题就集中在，如何对Mongodb数据进行分页，查询，获取对应的数据 
            - SQL代码1：平均用时6.6秒 SELECT * FROM `cdb_posts` ORDER BY pid LIMIT 1000000 , 30 
            - SQL代码2：平均用时0.6秒 SELECT * FROM `cdb_posts` WHERE pid >= (SELECT pid FROM 
              `cdb_posts` ORDER BY pid LIMIT 1000000 , 1) LIMIT 30
2019.08.14 - 看下如何使用redis设置时间，一定时间过后就删除对应的数据  -- 设计：redis存入时间为访问的时间，时间超过一个月没有二次访问就删除
2019.08.12 - from scrapy.interfaces import ISpiderLoader - from zope.interface import implementer - @implementer(ISpiderLoader) - 这是个什么骚操作，接口吗?
2019.08.12 - 爬虫是在哪一步被实例化的，什么时候会执行__init__初始化函数。在init之前，执行了一次update_setting，对custom_setting进行了初始化，所以把custom_setting写在init里面是没有用的，但是把heartbeat写在init里面，这个倒是没有问题
2019.07.27 - 创建mongodb用户
            db.createUser({user:'admin',pwd:'admin',roles:[{role:'userAdminAnyDatabase',db:'admin'}]})
            db.auth("user","password")
            mongodb://user:password@localhost:27017/admin 
2019.07.27 - 完成proxy—pool开源项目 https://github.com/CzaOrz/ioco/tree/t426/open_source_project/proxy_pool/
2019.07.19 - 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware' 爬虫代理，我的天哪，我居然还不会，醉了。代理是个大问题啊！
        url_list = ['http://www.xicidaili.com/nn/',  # 高匿 'http://www.xicidaili.com/nt/',  # 透明 ]
        url_list = ['https://www.kuaidaili.com/free/inha/','https://www.kuaidaili.com/free/intr/']
2019.07.22 - blog模板苏沪有点问题
2019.07.19 - 二叉树的三种排序
2019.07.21 - 自如改版，价格居然放在了css里面，真是无语
2019.07.18 - 可以对文章进行分类，再来一个汇总的，这样就很nice了，还需要见一个数据库做统计分类
2019.07.18 - 删除评论模块有BUG，只删除了父评论，子评论还在！！！！
2019.06.04 - 百度那位小哥的代码，看看是不是可以加入Item组件，感觉很牛
2019.07.17 - scrapy如何停止，这是个问题
2019.07.14 - sx富文本编辑器，使用了Vue的初始化等没怎么建国的函数，尝试了解然后部署到自己机器上把，哈哈哈
2019.07.17 - 直接调用别人的js，太贱了吧，哈哈哈，害怕
2019.07.15 - Vue的几个实例，研究研究，copy过来，很吊哦
2019.07.15 - 为网站添加反爬机制 - 添加最简单的cookie反爬，后期看是否有必要再深入
2019.07.15 - root用户管理界面有问题，访问500
2019.07.12 - 如何关注前沿知识，什么是持续跟进一个项目？？？？  -- 居然还是在github上面找，哎，哪里找得到啊
2019.06.03 - md说明文件的编写规范与格式
2019.06.13 - pdf2html这个处理下 https://blog.csdn.net/silentacit/article/details/80309929
2019.06.17 - 工作所需：scrapy基本原理、反爬知识（涉及js重定向，加密，投毒等）、爬虫selenium模块、后端aiohttp、flask、Django模块，前端js，Vue模块，简单的异步实现
2019.07.03 - fiddler抓包工具到底怎么用啊啊啊啊啊啊啊啊啊   网易云爬虫 - https://www.jianshu.com/p/a45714d16294-
2019.06.25 - 前端页面太牛逼了，各种游戏！！！！！可以看看最后一页  -- 可以，见识到了各种牛逼的操作，前端是一个无底洞，知识太多了
2019.06.03 - redis集群，这个怎么玩啊  -- 集群这玩意暂时用不到啊
2019.05.29 - 解析附件部分代码需要整理docx，excel  -- 解析附件再见吧宝贝
2019.06.03 - 附件转化，doc转docx，pdf转html，还有pdf的相关操作，这些我是不是写过啊，再整理一下吧
2019.07.02 - IOCO爬虫流程图，可以用md文件写了放在首页啊，nice啊马飞
2019.01.12 - 前段炸裂特效，，这个需要从长计议啊，怎么展示是个问题
2019.06.18 - scrapy.extensions.logstats，scrapt的extension快怎么使用
2019.06.25 - src="../js/echarts.min.js"，数据可视化的插件https://www.echartsjs.com/tutorial.html这个太牛逼了      axios.min.js 是Vue的插件，异步请求。化柱形图和折线图，暂时只需要这两个把。
2019.06.26 - 插入视屏是个啥玩意：<video src="http://vjs.zencdn.net/v/oceans.mp4" type="video/mp4" autoplay="autoplay" controls="controls" loop="-1" poster="false.png">
2019.06.06 - <input type="text" ref="input1"/>  this.$refs.input1.value ="22"; 减少获取dom节点的消耗  - Vue props, mounted()
2019.06.25 - 在首页做一个统计算了，博客统计，访问统计、爬虫统计，然后最下面放一些细分模块。得好好想象到底怎么部署整个页面。
2019.06.24 - IOCO动图有BUG，左边评论栏也有bug，这玩意居然在屏幕缩小后出现在下面
2019.06.17 - 算法题，各种计算机基础（算法原理，计算机基础），太重要了把，你只会一些大家都有的东西有什么意义，Django，Flask等，都太普遍了，意义是找工作，而且也只能去打杂的工作！
2019.06.23 - 后序涉及到如何上传如片了，如何在手机端进行较良的展示，太丑了，好吧，电脑端也丑，那就以电脑为起始进行优化把。主要是脑子里就没有思路，重来没有好好勾画过整个结构
2019.06.17 - 工作经历：中软是测试，测GPS、充电、开关机，舆情日报，AndroidStudio。数博科技：爬虫工程师，
2019.06.17 - 对scrapy的理解还是不深，很多都不会
2019.06.02 - 爬虫框架中还有raise Exception模块需要写，对各种异常的定义，要个性化一点
2019.06.03 - Scrapy框架signal模块是个什么原理，怎么实际开发中还能用的到，怎么用，参考巨潮年报
2019.07.11 - 爬虫工厂可以放一些数据分析解析出来的图片，这个是不是可以弄一个缓存机制?
2019.06.12 - 爬虫的数据分析结果，可以将分析结果返回，传到前段，这个怎么搞
2019.06.12 - 介绍resume.html页面（写一写历史线就差不多了=0=）
2019.07.02 - 不能舍进求远，自己的框架有大问题，scrapy怎么会跳转这么慢，把其他逻辑偶读好好完善下，问题越来越多了
2019.07.09 - 呵呵，居然定时任务不会启动，真是醉了，今天再研究研究吧没改写爬虫了，没有输出
2019.06.12 - （首先新的爬虫可以开始看看了，以先看职位，如boss直招和智联招聘这两个，房天下爬虫也可以看看，那么爬虫就有4个了）
2019.06.12 - 3个新爬虫（boss直招、智联招聘、房天下，共计四个在线爬虫）。
2019.06.12 - 今天再把搜索功能移植过去，基本已有的就都OK了，然后就是添加新的功能。
2019.07.09 - 能不能部署心跳啊，感觉怪怪的，把邮件模块去除把，这个定时真是搞事，要不今天搞定?
2019.07.03 - pip install pycryptodome 安装网易云解析音乐的爬虫包.
2019.07.01 - 现阶段的主要任务就是编写文档，储存补给站 -- 文档卸载这边感觉不太合适啊，可以适当的卸载博客园里面吧
2019.07.03 - "select name from sqlite_master where type='table' order by name"  -- 神奇的sql指令
2019.07.01 - 发展历史线，可以使用ol/li有序表？还是ul无序表
2019.06.30 - 邮件模块记得拿到手，别浪费了
2019.06.18 - 微信可以了解验证码，微博可以练selenium -- 没有遇到验证码，说明有cookie，下午可以试一试
2019.06.26 - 监听回车键进行登陆完成
2019.06.24 - wangEditor 富文本编辑器  background-color: #f4f3f4  xs 使用的背景颜色，很好看啊，浅灰色
2019.06.25 - 富文本编辑器有一个坑，我似乎没法获取文本内容，阿卡宁夏xs泽呢么获取的，怎么获取怎么编辑。图片视频什么都可以直接插入，神奇
2019.06.26 - python邮件功能发出去
2019.06.25 - 添加统计模块 - alter table blogs add count bigint not null default 0;
2019.06.03 - 现在的框架不支持post请求下载，这个显然不太合理，可以研究研究怎么下载post请求的数据 - post请求就算了，这种直接存为bytes
2019.06.05 - 关于各高校高考分数的信息，可以做一个数据分析，这个就没必要做持续，因为每年就一次高考，或许可以提供某些服务。爬985高校，211高校
2019.06.05 - 前端那种折线图，动态展示是怎么做的啊，折线，柱状图，饼状图等等 - js搞定，不会，但是会扣
2019.06.06 - 各高校的分数等情况，是时候提上日程了 - 反爬没搞定==
2019.06.11 - 绘图软件SAI，怎么说 - 打扰，应该比想象中的难
2019.06.22 - 如何在右上角显示最新评论，这个可以有，或者可以设置点赞评论?
2019.06.23 - # -*-coding: utf-8-*-
2019.06.17 - bootstrap wysiwyg 富文本编辑器
2019.06.18 - 普通用户管理界面的完善，博客如何添加其他字体或文本，富文本编辑器?
2019.06.18 - numberAnimate数字滚动插件, 动态折线图 https://www.html5tricks.com/html5-canvas-animated-line.html,  临时https://blog.csdn.net/vhwfr2u02q/article/details/79492303
2019.06.18 - 评论回复并拼接是如何实现的
2019.06.21 - 子评论时间bug
2019.06.17 - 博客编辑页面，root管理博客页面，个人管理个人博客页面
2019.06.05 - bs还是需要重新再看一遍啊，这次只看那些细节，我发现似乎只需要name点东西就可以拼出我想要的，如首页三列，左边是章节内容栏，右边是导航栏目，侧滑菜单是大方向，中间是内容
2019.06.05 - 正则学习，零宽断言 -- re.compile("var\s+(rand\d+)\s*=\"(.+?)\";(?=[\s\S]+document\.write\(\"(.+?)：.+\"\+\\1\+)") 零宽断言，中间居然能隔这么远，这已经是扣了
2019.06.02 - BoopStrap/JavaScript插件
2019.05.30 - 用户注册和登陆模块，前端的编写，后端需要在整理整理，别的不说，起码把注册页面再次搞出来把
2019.06.11 - 百度地图模块
2019.06.12 - Vue的学习
2019.06.12 - Jquery学习
2019.06.11 - inspect模块害的再斟酌斟酌
2019.06.03 - scrapy如何增加日志模块，可以在下载中执行指令-s LOG_FILE= --loglevel=INFO来启动吗
2019.06.04 - 廖老师的git和sql还是要再看看啊，这玩意有用的很
2019.06.03 - 如何使用logging模块兵输出具体的文件 from logging.handlers import TimedRotatingFileHandler 模块
2019.06.02 - BoopStrap组件
2019.06.03 - window下如何开启定时任务
2019.06.03 - 百度那位小哥的模拟Scrapy框架，可以学习学习精髓，有点小经典
2019.06.02 - 爬虫框架解析部分多线程或者多进程跑。- 对每一个线程传入标记位，以id最后一位作为判断计算此任务属于哪个线程，从而人为分配任务而非操作系统分配
2019.06-02 - BoopStrap全局CSS样式
2019.05.29 - 中国裁判文书网，对key的获取，需要处理
2019.05.30 - scrapy的deffer，或者说twisted模块如何使用
2019.05.31 - Failure - 该框架，解析部分是否可以使用异步，下载部分是否有必要使用异步。异步是使用twisted还是使用简单的async，这两个那种好一点，可以先研究上面的twisted再下结论
2019.05.31 - 把相应的js反爬，写一个中间件可以，name每次只需要调用该中间件即可，而不是每个模块都去写一遍处理逻辑
2019.05.29 - 把对计算云的辅助操作单独写一个模块，包含压缩与推送
2019.05.30 - 对工具进行适当地整理，把不要的删除，或者重新命名整合下
2019.05.30 - scrapy中间件需要在写一个模块，用于熟悉与练习
2019.05.30 - 计算云中新建线上环境的git仓，用于部署，还有专门链接文件的仓。即一个专门接受文件，用于链接这里面的文件，来实现部署
2019.05.30 - 今晚学习了集中算法冒泡、直接插入、希尔排序、快速排序、简单排序
"""

"""不错的学习平台
html学习平台        https://www.html5tricks.com/
js转化平台          http://tool.oschina.net/codeformat/js    
爬虫学习            https://github.com/Jack-Cherish/python-spider/commit/10610ab354fc1bb8264edc566766df6588111914     https://cuijiahua.com/blog/ml/
百度AI开放平台      https://ai.baidu.com/docs#/Face-Detect-V3/top
JS                  https://github.com/SUNNERCMS/30daysJavascript
17素材网            https://www.17sucai.com/
JS前端              https://github.com/phodal/sherlock

"""

"""不错的个人网站
专注机器学习、爬虫        http://www.lining0806.com/
爬虫写的很秀              https://github.com/FanhuaandLuomu
Jack Cui                  https://cuijiahua.com/blog/ml/
"""

"""645948
You Are An Apple In My Eyes
Courage is not the absence of fear, but rather the judgment that something else is more important than fear.
所有渴望别人理解的行为都是弱智的行为，人的强大第一步，要学会孤独，第二步，要学会不理解，第三步，用结果去碾压
你的压力来源于，无法自律的内心而只是假装努力，现状跟不上内心的欲望，所以你焦虑升值恐慌
只靠理想的话，世界是无法运转的
"""

"""2019 ULTIMATE PLANING
爬虫框架重构
前段代码整合
爬虫调度器需要解耦，除了定时任务之外，还需加入调度池引入优先级的说法。定时任务和调度任务是两回事吗。

"""
