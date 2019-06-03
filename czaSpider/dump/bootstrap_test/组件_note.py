__goal__ = "Note for 前端组件"
"""
span中可以通过添加class展示各种图标，当需要增加文本时，务必在图标和文本之间添加一个空格
<span class="glyphicon"> Star  就像这里一样，前面需要加空格

弹窗里面可以加图标

【下拉菜单】
下拉菜单触发器和下拉菜单都包裹早dropdown里面
按钮那一块使用class="dropdown"，而具体的下拉内容我们应该使用class="dropdown-menu"属性
整个模块都可以扔到<div>里面去，整个下拉就是一个div模块
菜单的内容默认是左对齐的，通过<ul class="dropdown-menu dropdown-menu-right">可以让菜单那右对齐
这里的右对齐就是整个框都到右边去了的意思，不是字体在右边

可以在这个div的首行加入标题来表达这个菜单栏的意思，首行就是在ul的意思，不是在整个div
<li class="dropdown-header">DropDown</li>
还可以添加分割线：<li role="separator" class="divider"></li>这就是一条分割线


【按钮组】
是一个div模块，这个模块为class="btn-group"，当有唐初框是，必须指定container：'body'属性
还需要确保设置正确的role属性并提供一个label标签，按钮组就是role="group", 对于工具栏就是class="toolbar"
<div class="btn-group" role="group"></div>
<div class="btn-toolbar" role="toolbar"><div class="btn-group" role="group"></div></div>在里面组合进group，同样也是可以的，这样就是分开了而已，感觉没和在一起的好看
class="btn-group btn-group-lg"可以设置按钮组的大小

可以组合按钮组和下拉菜单组，就是把group里面且套一个group，然后把下拉菜单的属性扔进去
通过btn-group得到的按钮组大小是随着字体的多少变化的，想要获得一个固定的不变的样式，我们可以使用justified
<div class="btn-group btn-group-justified" role="group"><div class="btn-group" role="group"> 通过这种外面是justified，里面嵌套btn-group来实现同一按钮组的大小

所谓的分裂是按钮，就是一个普通的下拉式按钮组，在前面再加一个无关紧要的按钮咯

【输入框组】
只支持input，不支持select，也不支持textarea，使用的class="input-group"
不要将表单或column直接和输入框混合使用，而是将输入框组嵌套入表单组或者栅格相关的元素
<div class="input-group"><span class="input-group-addon">@</span><input class="form-control" type="text" placeholder="Username"></div>
可以直接通过对<div class="input-group input-group-lg">调整整体的大小而不是单独的去调整每一个

作为额外元素的按钮，即使用input-group-btn而不是input-group-addon
这种其实就是在一个div为row的模板里面，对col记性响应的设计，里面嵌套input-group
按钮的大小可以使用class="form-control"来进行控制，默认的大小就那样啊
<div class="row"><div class="col-lg-6"><div class="input-group"><input><span class="input-group-btn"><button>
我去，怎么感觉都有点大同小异了

【导航】
，如果在导航组件实现导航条功能，务必在ul的最外围的逻辑上加上role="navigation"
普通标签页，使用<ul class"nav nav-tabs"><li role="presentation"></li>
胶囊式标签，使用<ul class="nav nav-pills">，区分不同的状态，可以使用class="avtive"，这个估计得使用js了
垂直式标签，使用<ul class="nav nav-pills nav-stacked">
当你需要等宽的时候，可以使用nav-justified
ul里面接li，而li里面则接a，所以当你需要使用下拉菜单的时候记得用a而不是button，type=button

【导航条】
一般导航条都使用nav标签，如果使用的div的化，我们应该使用role="navigation"
对于导航条，使用<nav class="navbar navbar-default">
里面就是一些乱七八糟的东西，感觉和以前额都不太一样了

你想要创建一个header，需要先创建一个container-fluid，在这里面进行一些配置
如<div class="container-fluid"><div class="navbar-header"><a class="navbar-brand"><img src="#"></a></div></div>这个可是一路嵌套到最里层啊
navbar-header是服务于收个标签或者图片的，这个模块在container-fluid里面

<div class="collapse navbar-collapse"> 这个模块是用来手机超链接，表单还有一些下拉菜单等属性的，是一个与navbar-header同级的意思把

这里的导航都变了<ul class="nav navbar-nav">都变成这个样子了，醉了，以前的是<div class="nav nav-pills">

表单也变了<form class="navbar-form navbar-left">，里面还是使用form-group，基本都还好















"""






















