__goal__ = "js"

"""
''.length;                   // 获取字符串的长度
''.toUpperCase()             // 获取大写
''.toLowerCase()             // 获取小写
''.indexOf()                 // 搜索指定字符串出现的下标，没有找到指定的子串，返回-1
''.substring()               // 返回指定索引区间的子串。可以想成python的切片。(0,7)表示0-7, (7)表示从7开始到结束
array.length                 // 获取数组的长度。不要随意对数组长度进行修改，这玩意居然会对原数组造成影响。直接通过索引进行处理，超过索引的也可以处理，这..
array.indexOf()              // 同样可以通过indexOf查询目标，没有找到，返回-1
array.slice()                // 可以理解为切片了。可以简单实现copy功能。NewCopy = array.slice()
array.push()                 // 操作尾部元素
array.pop()                  //
array.unshift()              // 操作头部元素
array.shift()                // 把头部元素删除
array.sort()                 // 按顺序排序，也就是从小到大
array.reverse()              // 反转该数组
array.splice()               // 万能方法。前两个数字分别表示下标和数量，弱需要添加则从第三个参数开始写起。(2,1,'test')从下标2删除1个并添加test，(2,0,'test')表示不删除只添加
array.concat()               // 合并两个数组。[1,2,3].concat(4,5,[6,7])居然会自动拆开里面的数组，直接合并为新数组
array.join()                 // 组合字符串的方法。[1,2,3].join('-')
delete a.age                 // 删除对象的属性
'age' in a                   // 判断对象a中是否存在属性age（对象就相当于是个字典嘛），但是此方法可能不是来自a对象本身的，也有可能是来自其他父类
a.hasOwnProperty             // 该方法用于判断是否是自身的属性而不是继承得到的
for (i=0, i<a.length, i++)   // for循环语法，此处是循环一个数组的写法
for (;;)                     // 表示无限循环
for (var key in array)       // 循环某个数组把数据都拿出来
while (n > 0) {...}          // while循环
new Map([['a', 1],])         // 创建一个map对象，可以理解为一个字典嘛
map.set('a', 1)              //
map.has('a')                 // 返回bool
map.get('a')                 // 获取属性，不存在则返回undefined
map.delete('a')              // 删除属性
new Set([1, 2, 3, 3])        // set集，去重
set.add(4)                   // 添加
set.delete(3)                // 删除
for (var key of MapOrSet)    // 一般遍历数组，但是对于Map和Set也属于可迭代类型，他们无法使用for+in，但可以使用for+of。Map返回是数组两个值，Set就一个值。for+of优于for+in
array.forEach(function(ele, index, source){...})  //最多可以输入三参数或者随意，第一个元素表示目标元素，第二个表示下标索引，第三个表示原数组。MapSet均支持，此方法最优先。但是Map中的分别表示：value/key/source
array.forEach((x,y,z)=>{..}) // 箭头函数
...rest                      // 类似python中的*argv,kwargs，
var {a,b:new_id} = person;   // 快速赋值，直接抽取person对象中的a和b属性，进行赋值，若没有对应属性则赋值undefined。也支持查询后的快速赋值，此处为new_id
var {a=true} = person        // 还支持默认赋值，也就是没有查找到的时候赋值为true
({a=true} = person)          // 当a在此之前已经被声明了，则直接赋值会报错，应该使用()括号包起来
[x, y] = [y, x]              // 和python中的 x,y = y,x 一个意思
var {hostname:domain, pathname:path} = location;  // 快速获取当前页面的域名和路径。卧槽WC这个太狠了。
(function (x) { return x*x })(i)                  // 这是一个匿名函数。对应着python中的 lambda x: x*x
var fn = x => x * x;         // 箭头函数看着也好难受。箭头函数优于匿名函数，修复了this指向问题，总是指向外层调用者而不是单独开一个域出来
(x, y) => x + y              //
() => 3.14159                // 无参数
(x, y, ...rest) => x         // 可变参数
x => ({ foo: x })            // 单独返回一个对象需要使用括号
function* foo(x) { yield x } // 生成器generator 
generator.next()             // 调用方法 返回一个这么奇怪的东西{value: 0, done: false} 这种就需要自己手动判断下生成器是否结束，也就是判断done为true
for (var x of generator)     // 使用for+of实现
parseInt()                   // parseInt('123')
parseFloat()                 // parseFloat('123')
String()                     // String(123)
toString()                   // 123..toString()不能直接点，会报错，或者使用括号(123).toString()
Array.isArray(arr)           // 判断Array的方法
typeof window.myVar === 'undefined'                // 判断全局变量是否存在
new RegExp('ABC\\-001').test('cza')                // 正则 test表示是否匹配
/^\d{3}\-\d{3,8}$/.test('cza')                     //
/^\d{3}\-\d{3,8}$/g.exec('cza')                     // 分组，后面的g表示全局匹配。第一个元素是整个字符串，后面才是匹配到的数据
JSON.stringify()             // 
JSON.stringify(obj, null, ' ')  // 输出好看点
JSON.stringify(obj, ['name', 'skills'], ' ')  // 可以指定输出，也可以传入函数处理键值对
toJSON                       // 定义此方法后只输出对应的属性
JSON.parse()                 // 反序列化
Student.prototype            // 可以直接得到Student的构造函数
class Son extends Fat { constructor(name){super(name);} hello(){alert('hello world');} }
"""
"""
var Student = { name: 'cza', height: 1.5 }
var hj = { name: 'csa' };
hj.__proto__ = Student;  // 把hj的原型指向了对象Student，就是hj是从student继承得到的一样。构成了一个原型链 （prototype: 原型的单词）。当然这是错误的方法

创建对象，使用new
function Student (name) { this.name=name; this.hello=function () { alert('hello'+name); } }
s = new Student('cza')
s.constructor  // 指向函数Student本身
xiaoming.constructor === Student.prototype.constructor; // true，Student.prototype.constructor这玩意就是指向本身嘛，没什么意义
Student.prototype.constructor === Student; // true。原来是他们公用一个构造函数。小明和学生都共同维护一个constructor构造函数
比如这个时候盗用s.__proto__，我们得到不是Student，而是Student的构造函数constructor，更骚的是Student的prototype也是这玩意
其实不用想的name复杂，一个对象Student，创建实例小明，那么小明的原型对象就是Student的构造函数，而不是Student本身，他本身有一个prototype可以找到这个对象，这个对象也有constructor可以找到Student。
用python来解释就是class Student:... 小明=Student() 创建一个实例后，小明就是Student的一个实例，Student()可以使用__class__找到原类。这里的__class__就是constructor，这个prototype就是实例化，这

原型继承：用最新的class算了，以前的打扰
class Student {
    constructor(name) {
        this.name = name;
    }
    hello() {
        alert('cza')
    }
}
class SonStudent extends Student {
    constructor(name, grade) {
        super(name);
        this.grade = grade;
    }
    myGrade() {
        alert('cza')
    }
}

$(document).ready(function () {
    // on('submit', function)也可以简化:
    $('#testForm).submit(function () {
        alert('submit!');
    });
});
$(function () {
    // init...
});
"""
"""
JS的对象对应着python中的dict。绑定到对象上的函数称之为方法。在函数中使用this会指向当前对象，没有话会指向全局变量window
不适用var声明变量则会变为全局变量，这样很nice呀
var申明的变量实际上是有作用域的，像我之前都是在函数内部声明，故得到的都是一个局部变量，无法作用在外部
实际上就是默认有一个window的全局作用域。所以实际上JS只有一个全局作用变量就是window

let替代var可以申明一个块级作用域的变量
for (let i in array) {...}这里的i则只是在块中起作用
const与let都具有块级作用域，且不可修改嘛

当你声明了无效的变量，需要添加''来表示
JS函数附带一个arguments参数，用于获取或判断传入参数的个数以便后续处理
function test(a, b, c) {
    if (arguments.length === 2) {
        c = b; b = null;
    }
}

装饰器?
var count = 0, old = parseInt;
window.parseInt = function () { count+=1; return old.apply(null, arguments); }

闭包:  怎么会这样啊，看着真是难受
function count(init) {
    var x = init || 0;
    return { inc: function () { x += 1; return x; } }
} 
"""
"""
var now = new Date();
now; // Wed Jun 24 2015 19:49:22 GMT+0800 (CST)
now.getFullYear(); // 2015, 年份
now.getMonth(); // 5, 月份，注意月份范围是0~11，5表示六月  对象月份值从0开始，牢记0=1月，1=2月，2=3月，……，11=12月。
now.getDate(); // 24, 表示24号
now.getDay(); // 3, 表示星期三
now.getHours(); // 19, 24小时制
now.getMinutes(); // 49, 分钟
now.getSeconds(); // 22, 秒
now.getMilliseconds(); // 875, 毫秒数
now.getTime(); // 1435146562875, 以number形式表示的时间戳

location.protocol; // 'http'
location.host; // 'www.example.com'
location.port; // '8080'
location.pathname; // '/path/index.html'
location.search; // '?a=1&b=2'
location.hash; // 'TOP'
"""


"""
通过内置的data-API可以使用所有的js插件
【模态框】
能够动态谈下来的那种框框，使用的class="modal fade" role="dialog" data-dismiss="modal" aria-label="Close"
首先是一个大类<div class="modal-dialog" role="document">用来包括所有的内容
然后用一个<div class="modal-content">来包括所有的内容
里面的细节就是class="modal-header" / "modal-body" / "modal-footer"

这个务必添加role和aria-labelledby属性，且需要在标题中的按钮中添加aria-hidden="true"属性
这里的fade是用来控制淡入淡出的，很好看啊
class="modal fade" role="dialog"
    class="modal-dialog" role="document"
        class="modal-content"
            class="modal-header"
            class="modal-nody"
            class="modal-footer"
如果要添加栅格栏，或者表单，我们可以在body里面进行定义

【dropdown】
$('#myDropdown').on('show.bs.dropdown', function(){
    //do something
})

实现动态切换，可以使用
$('#myTabs a').click(function(e){
    e.preventDefault()
    $(this).tab('show')
})
$('#myTabs a[href="#profile"]').tab('show')
$('#myTabs a:first').tab('show')

可以对按钮添加动态信息
<button type="button" class="btn" data-toggle="tooltip" data-placement="left" title="Hello World">


nav nav-sidebar

"""



"""echarts note
title: { // 图的标题
    text: '补给站'
},

legend: { // 图的说明栏，可以定义在左边或右边
    orient: 'vertical',
    x: 'left',
    data:['直接访问','邮件营销','联盟广告','视频广告','搜索引擎']
},


"""

""" 上传本地文件的方法
var
    fileInput = document.getElementById('test-image-file'),
    info = document.getElementById('test-file-info'),
    preview = document.getElementById('test-image-preview');
// 监听change事件:
fileInput.addEventListener('change', function () {
    // 清除背景图片:
    preview.style.backgroundImage = '';
    // 检查文件是否选择:
    if (!fileInput.value) {
        info.innerHTML = '没有选择文件';
        return;
    }
    // 获取File引用:
    var file = fileInput.files[0];
    // 获取File信息:
    info.innerHTML = '文件: ' + file.name + '<br>' +
                     '大小: ' + file.size + '<br>' +
                     '修改: ' + file.lastModifiedDate;
    if (file.type !== 'image/jpeg' && file.type !== 'image/png' && file.type !== 'image/gif') {
        alert('不是有效的图片文件!');
        return;
    }
    // 读取文件:
    var reader = new FileReader();
    reader.onload = function(e) {
        var
            data = e.target.result; // 'data:image/jpeg;base64,/9j/4AAQSk...(base64编码)...'            
        preview.style.backgroundImage = 'url(' + data + ')';
    };
    // 以DataURL的形式读取文件:
    reader.readAsDataURL(file);
});
"""
