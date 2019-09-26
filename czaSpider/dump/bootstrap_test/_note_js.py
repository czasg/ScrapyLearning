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
var {hostname:domain, pathname:path} = location;  //快速获取当前页面的域名和路径。卧槽WC这个太狠了。
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


