__purpose__ = "Note For Html"

"""
布局容器
需要为【页面内容】和【栅格系统】使用.container容器，这二者不能相互嵌套
<div class="container"> 类似固定宽度并支持响应式布局的容器
<div class="container-fluid"> 类似于100%宽度，占据全部视口（viewport）的容器

【栅格系统】
栅格系统就是通过一系类行row和一系列column的组合来创建页面布局。 说白点就是行列组成的嘛
row必须在.container（固定宽度）或者.container-fluid（100%宽度）中，方便排列aligment和内补padding
column置于row中，每一个column用于放置内容，且只有column可以作为row的直接子元素
可以通过对列设置padding内补属性，从而创建列与列之间的间隔
通过为row设置负值margin，从而抵消为container元素设置的padding
.col-xs-4表示三个等宽列

标签：
<mark>表示标记文本
<del>表示删除文本
<u>表示有下划线的文本

class="text-left", "text-center", "text-right", "text-justify", "text-nowrap"
分别表示左对齐、中间对齐、右对齐、
class="text-lowercase", "text-uppercase", "text-capitalize"
分别表示字体的大小

<abbr title="allow">al</abbr>表示略缩语，鼠标过去会显示所有的
<blockquote>表示引用
<dl><dt><dd>这三个表示带有描述的短语列表
<code>表示代码片段
<kbd>表示用户输入字段，参考linux终端输入

class="table" 
class="table table-striped" 添加斑马状表格
class="table table-bordered" 为每一个表格添加边框
class="table table-hover" 让每一行对鼠标悬停做出响应
class="table table-condensed" 让表格更加紧凑
<div class="table-responsive"> 创建响应式表格，即允许其在屏幕上水平滚动，需要将table放到这里面

【表单】
单独的表单有一些全局样式，所有设置了form-control类的标签（input，textarea，select）都会成为宽度100%
将这些空间放置到<div class="form-group">类中，可以自动获得最好的排列
一定要设置label，就算不想要也要设置，可以使用sr-only隐藏
class="form-inline"表示内联表单，即内容做对齐，此时lable与input是上下关系
class="form-horizontal"表示水平表单
<div class="input-group"><div class="input-group-addon">@</div></div>可以预填文章

对多行的表单文本控件，可以更改rows属性来实现，也就是我想要一个大一点的输入框，可以使用rows属性
如<textarea class="form-control" rows="3"></textarea>

单选多选框，<div class="checkbox"><label><input type="checkbox">hello world  都是向这种样式的编写方法
对lable设置type="checkbox-inline"可以使控件排成一行

下拉框
<select class="form-control"><option>1</option></select>通过添加多个option可以实现
当你使用了multiple时，默认会显示多选项<select multiple class="">

为输入框设置disable可以禁用此输入框
class="input-lg input-sm" 可以控制输入框的大小

水平排列输入框<form class="form-horizontal"><div class="form-group"><label class="col-sm-2"><div class="col-sm-10"><input class="form-control">
即首先是一个form表示表单，再一个div包含form-group，通过设置label和div的col属性，可以达到多个标签在同一列的表现
还可以通过row来实现排列在同一行，即row一下，对然后只对div设置col-xs属性等，每个属性里面可以方label和input属性

【按钮】
<button class="btn btn-default" type="submit">
<input class="btn btn-default" type=button>
如果要用a标签，则需要将其设置为role="button"
btn-sm，btn-lg，btn-xs可以设置按钮的大小，外形上的大小
btn-block我可以让按钮填充整个父级元素，即100%

【图片】
响应式图片<img src="" class="img-responsive">
若要使图片居中，可以使用center-block，而不是text-center
class="img-rounded", "img-circle", "img-thumbnail"分别代表圆角正方形，圆形，正方形

对于文本p标签，我们可以让他有不同的颜色class="text-warning"这是是仅仅针对文字的
如果是想要修改文本的背景颜色，我们可以使用"bg-primary bg-warning"

左右浮动
<div class="pull-left pull-right">可以将任意元素向左或向右浮动，居中则是<class="center-block">
当时上述不能用于导航条中，在导航条中可以使用class="navbar-left navbar-right"






"""