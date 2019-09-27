__file__ = ''

"""
<!DOCTYPE html>
<html lang="zh-CN"></html>                                   //前提设置
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">    // 支持移动设备，其中user-scalable表示禁止用户缩放
col-xs-12                                                    // auto
col-sm-12                                                    // 750px
col-md-12                                                    // 970px
col-lg-12                                                    // 1170px
col-sm-offset-2 col-md-offset-0                              // 偏移。有必要时，后面应覆盖前面
<h1><small></small></h1>                                     // 这种字体挺漂亮的
<blockquote><p></p></blockquote>                             // 表示引用，里面最好用p
<dl class="dl-horizontal"><dt><dd></dl></dt></dd>            // 带有描述的短语列表，dt是加粗的标题，dd是内容
<form><div class="form-group"><label></label><input type="text"></div><button type="submit"></button></form>  // 每一个input都需要from-group
<textarea class="form-control" rows="3">                     // 文本域
<div class="checkbox"><label><input type="checkbox"></label></div>
<div class="checkbox"><label><input type="radio" name="only-name"></label></div>  // 对于圆点，只要定义同一个name就ok了，保证唯一
<select class="form-control"><option>1</option></select>     // 下拉列表
<span class="caret"></span>                                  // 下三角符号
<div class="clearfix"></div>                                 // 清除浮动
<button><span class="标签"></span></button>
<div class="btn"><button><div class="btn-group">   // 按钮组内的下拉菜单需要放到一个btn-group中
<div class="btn-group btn-group-justified"><div class="btn-group">  // 需要btn-group里面嵌套btn-group
<div class="dropdown">  // 下拉菜单
<div class="btn-group"> // 按钮式下拉菜单
<div class="btn-group"><button><button><ul>  // 这就可以形成分裂式按钮下拉菜单
<div class="input-group"><input><span class="input-group-btn"><button>  // 在输入框组中作为额外的按钮


class="lead"                                                 
class="text-left"
class="text-center"
class="text-right"
class="text-lowercase"
class="text-uppercase"
class="text-capitalize"
class="table-bordered table-hover table-condensed table-responsive"
class="form-control"  // width: 100%;
class="form-group"
class="form-inline"   // 内联表单，也就是显示在一行内咯
class="input-group-addon"  // 放在input前面或者后面，可以实现固定输出显示
class="input-group"        // 用来与class="input-group-addon"组合的
class="form-horizontal"    // 定义水平表单，在这里每一个form-group就是一行。一行内可以使用col-sm-2来设定对应的大小
class="checkbox-inline"
class="radio-inline"       // 这个是用造label中的，包裹input就可以
class="btn-block"          // 可以让按钮的width:100%
class="img-rounded"
class="img-circle"
class="img-thumbnail"
class="img-responsive"
class="text-primary text-success text-info text-warning text-danger"
class="bg-primary bg-success bg-info bg-warning bg-danger"
class="pull-left"   // 浮动，当时不能用于导航条中，应该使用.navbar-left
class="center-block"   // 让内容块居中
class="hidden"
class="show"
class="hidden-xs hidden-sm hidden-md hidden-lg visible-lg-12"  // hidden就是仅仅隐藏哪一个，而visible就是仅这一行，没padding都没有吗
class="btn-group-vertical"  // 垂直堆叠排列显示的按钮组
class="nav nav-tabs"    // 用于ul标签，比较普通的标签页
class="nav nav-pills"   // 也是用于ul，这个就是胶囊式标签
class="nav nav-pills nav-stacked"  // 垂直式的胶囊标签
class="nav-justified"  //配合上述nav使用，可以使用标签两段对齐
class="navbar-btn"   // 这玩意可以直接在bavbar中使用，会垂直居中
class="navbar-text"  // 可以直接用在文本中，通常使用p标签
class="navbar-link"  //费导航的连接
body { padding-top: 70px; }  // 推荐使用此，因为导航条会挡住
class="navbar-static-top"  //静止在顶部
class="label label-default"  // 用于span上，表示标签
class="badge"   // 表示徽章
class="page-header"  // 增加一个页头的样式
class="list-group"
class="list-group-item"

"""




"""全局CSS样式
<div class="panel panel-default">
    <div class="panel-heading"></div>
    <div class="panel-body"></div>
    <div class="panel-footer"></div>
</div>


<ul class="media-list">
    <li class="media">
        <div class="media-left">
            <a>
                <img src="", style="30*30">
            </a>
        </div>
        <div class="media-body">
            <h4 class="media-heading"></h4>
        </div>
    </li>
</ul>



<div class="alert alert-warning alert-dismissible" role="alert">
    <button type="button" class="close" data-dismiss="alert"><span>&times;</span></button>
    <strong>Warning!</strong>Please Check You Config
</div>  // 警告框，很有用

下拉菜单可以是
<div class="dropdown">  // 后接button或者a，然后就是下拉的内容
<div class="btn-group">  // 后接button，然后是下载的内容，一般都是ul+li
<ul class="nav nav-pills"><li class="dropdown">  // 导航里面只能接li了

页面设置为HTML5文档类型
<!DOCTYPE html>
<html lang="zh-CN"></html>

移动设备优先，其中user-scalable表示禁止用户缩放
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">


布局容器
.container   固定宽度并支持响应式布局，这个固定宽度可以说是非常棒了
.container-fluid   100%宽度，100%也不错呀

栅格系统
@media (min-width: @screen-sm-min) {/* 小屏幕（平板，大于等于 768px） */}
@media (min-width: @screen-md-min) {/* 中等屏幕（桌面显示器，大于等于 992px） */}
@media (min-width: @screen-lg-min) {/* 大屏幕（大桌面显示器，大于等于 1200px） */}
@media (min-width: @screen-sm-min) and (max-width: @screen-sm-max) { ... }
.col-xs-  这个xs有点意思，需要好好关注下的
.col-sm-  750px hidden-sm
.col-md-  970px
.col-lg-  1170px
col-sm-offset-  这玩意就相当于是一个占位符嘛。这个比我的好多了，我是直接蟹壳一个空的在哪里，这也太丢脸了吧，真low的写法
<div class="clearfix visible-xs-block"></div>当屏占比高度出现问题的时候，可以使用此行来消除高对不齐的情况，加了这个就可以按正常轨迹来执行
<div class="row">这个就很有意思了，在达到一定屏宽之前是固定宽度的，再小就是上面的屏占比为100%，下面的为50%，这就很nice了
    <div class="col-xs-12 col-md-8">.col-xs-12 .col-md-8</div>
    <div class="col-xs-6 col-md-4">.col-xs-6 .col-md-4</div>
</div>
<div class="row">这个也非常有意思，首先是8:4的屏占比，然后缩小会对应的缩小，再就是对半分，最后就是上面占比100%下面就是一半了
    <div class="col-xs-12 col-sm-6 col-md-8">.col-xs-12 .col-sm-6 .col-md-8</div>
    <div class="col-xs-6 col-md-4">.col-xs-6 .col-md-4</div>
</div>
<div class="row">偏移量，我可以理解为一种占位符col-sm-offset-，当前div偏移一定量的col-sm来达到目的。而且col-md-offset-0这玩意还一定要写哦，是用来覆盖前面的，不然后前面的偏移还是会生效
    <div class="col-sm-5 col-md-6" style="height: 400px; background: #C5CAE9;"></div>
    <div class="col-sm-5 col-sm-offset-2 col-md-6 col-md-offset-0" style="height: 400px; background: #FFF59D;"></div>
</div>
允许嵌套类，也就是col里面允许继续嵌套row，但是不支持container里面继续嵌套container-fluid，以前真是瞎搞呀
col-xs-12 col-sm-12 col-md-8老胡写的意思就是最小的时候是各自100%屏占比，sm的时候也是各自占100%，大一点的时候就是8:4了
col-xs-12 hidden-sm col-md-4 left-padding这个应该是读过源码的了，在sm的时候直接就hidden-sm隐藏了该栏目，再小的时候就恢复为100%

标题
<h1>h1. Bootstrap heading <small>Secondary text</small></h1>这里的小写字体还挺好看的，可以当做blog的标题
<p class="lead">...</p>
<code></code>这个是粉红色的，好蛮好看的呀

对齐
<p class="text-left">Left aligned text.</p>
<p class="text-center">Center aligned text.</p>
<p class="text-right">Right aligned text.</p>
<p class="text-justify">Justified text.</p>
<p class="text-nowrap">No wrap text.</p>
<p class="text-lowercase">Lowercased text.</p>
<p class="text-uppercase">Uppercased text.</p>
<p class="text-capitalize">Capitalized text.</p>

表格
<table class="table table-striped table-bordered table-hover table-condensed table-responsive">讲道理，这玩意应该就直接全部上去就可以了吧
"""

"""弹性布局
属性	描述
flex-direction	指定弹性容器中子元素排列方式  .flex-container { flex-direction: row | row-reverse | column | column-reverse; }
row	默认值。元素将水平显示，正如一个行一样。
row-reverse	与 row 相同，但是以相反的顺序。
column	元素将垂直显示，正如一个列一样。
column-reverse	与 column 相同，但是以相反的顺序。

flex-wrap	设置弹性盒子的子元素超出父容器时是否换行
nowrap	默认值。规定元素不拆行或不拆列。
wrap	规定元素在必要的时候拆行或拆列。
wrap-reverse	规定元素在必要的时候拆行或拆列，但是以相反的顺序。

flex-flow	flex-direction 和 flex-wrap 的简写  默认值为row nowrap。

align-items	设置弹性盒子元素在侧轴（纵轴）方向上的对齐方式
stretch	默认值。项目被拉伸以适应容器。
center	项目位于容器的中心。
flex-start	项目位于容器的开头。
flex-end	项目位于容器的结尾。
baseline	项目位于容器的基线上。

align-content	修改 flex-wrap 属性的行为，类似 align-items, 但不是设置子元素对齐，而是设置行对齐

justify-content	设置弹性盒子元素在主轴（横轴）方向上的对齐方式
flex-start	默认值。项目位于容器的开头。
flex-end	项目位于容器的结尾。
center	项目位于容器的中心。
space-between	项目位于各行之间留有空白的容器内。
space-around	项目位于各行之前、之间、之后都留有空白的容器内。

"""

"""
p、h1、div叫块级元素。定义为一个块，拥有块框
strong、span叫行内元素。定义显示在行内，拥有行内框

定位三种方式：
普通流、浮动流、绝对定位

普通流：元素框的位置由元素在HTML中的位置决定
块级框从上到下一个接一个垂直排列
行内框在一行中水平排列，框内元素不影响行框的高度

text-overflow: clip|ellipsis|string;

height:400px; overflow-x:hidden; overflow-y:scroll;  廖老师就这一句解惑
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

