__file__ = ''

"""全局CSS样式
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
