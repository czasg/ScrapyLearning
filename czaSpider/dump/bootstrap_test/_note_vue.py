__file__ = 'Vue学习笔记'

"""
$(function(){
    var vm = new Vue({  // 我可能用到的应该就是一下几种了
        el: '',
        data: {},
        computed: {},
        mounted: {},
        methods: {},
        
        el: '',
        data(){ return {} },
        computed: {},
        mounted(){ (async () => 匿名函数执行嘛)() },
        methods: {},
    });
    window.vm = vm;  // 这句话很重要
})

@keyup.enter="LOGINFunc"  // 按键监听 .up.down.left.right

mounted(){
    (async () => {
        var location = await isLogin();
    })()
}
"""

"""
过滤器函数{{ message | capitalize }}
filters: {
    test: function (value) { return '' }
}


计算属性computed，不如使用methods
methods，是函数调用，也就是调用的时候，需要实例化执行，如{{ method_fun() }}
computed，是属性调用，也就是调用的时候，不需要实例化执行，{{ computed_fun }}
第二最重要的一点是computed是带缓存的
相比大家都知道HTTP缓存，其核心作用就是对一些服务端未更新的资源进行复用，避免一些无谓的请求，优化了用户的体验
函数形式的调用，毫无疑问需要实例化多个对象，换句话来说就是你定义了多少个就需要执行多少遍
所以，官方文档才反复强调对于任何复杂逻辑，你都应当使用计算属性
computed依赖于data中的数据，只有在它的相关依赖数据发生改变时才会重新求值
那个你无论调用多少次，拿到的就是一个返回值，不会重新进行计算



监听属性watch  当监听的属性发生改变的时候，就会执行这个监控的函数
# 当有两个输入框的时候，我们可以只输入一个框，然后监听这个框，计算属性输出到另一个框，原来可以这样实现厉害了
vm = new Vue({el: '#id', data: {counter: 1}});
# 属于Vue之外的监控
vm.$watch('counter', function(newValue, oldValue) {  //两个值
    return
});
# 属于Vue之内的监控，直接对属性进行监控了啊
vm = new Vue({
    el: '#id',
    data: {
        a: 0, 
        b: 0
    },
    watch: {
        a: function (val) {this.a = 0; this.b = 0},
        b: function (val) {this.a = 0; this.b = 0}
    }
}) // 还可以添加二重监控，也就是与vm.$watch('')


按键修饰符 - Vue 允许为 v-on 在监听键盘事件时添加按键修饰符
<!-- 只有在 keyCode 是 13 时调用 vm.submit() -->
<input v-on:keyup.13="submit">
<!-- 同上 -->
<input v-on:keyup.enter="submit">
<!-- 缩写语法 -->
<input @keyup.enter="submit">
--------
.enter
.tab
.delete (捕获 "删除" 和 "退格" 键)
.esc
.space
.up
.down
.left
.right
.ctrl
.alt
.shift
.meta
--------
<p><!-- Alt + C -->
<input @keyup.alt.67="clear">
<!-- Ctrl + Click -->
<div @click.ctrl="doSomething">Do something</div>


v-bind:href  -缩写-  :href  // v-bind 绑定某个属性
v-on:click  -缩写-  @click  // v-on 绑定某个函数


v-if 指令将根据表达式 seen 的值(true 或 false )来决定是否插入 p 元素
v-else 指令
<div v-if="Math.random() > 0.5"></div>
<div v-else-if="type === 'B'"></div>
<div v-else></div>


在Vue中定义的方法，我们也可以在js中执行，如: vm.testFunc()  -- 可以执行执行对应的方法


复选框
type="checkbox"  -- 单选框，对应bool值  -- 复选框，对应数组[]


组件
Vue.component(tagName, options)
# 全局组件
<div id="app">
    <runoob></runoob>
</div>
<script>
// 注册
Vue.component('runoob', {
  template: '<h1>自定义组件!</h1>'
})
// 创建根实例
new Vue({
  el: '#app'
})
</script>
---------------------------------
# 局部组件
<div id="app">
    <runoob></runoob>
</div>
<script>
var Child = {
  template: '<h1>自定义组件!</h1>'
}
// 创建根实例
new Vue({
  el: '#app',
  components: {
    // <runoob> 将只在父模板可用
    'runoob': Child
  }
})
</script>
---------------------------------
# Prop属性
<div id="app">
    <child message="hello!"></child>
</div>
<script>
// 注册
Vue.component('child', {
  // 声明 props
  props: ['message'],
  // 同样也可以在 vm 实例中像 "this.message" 这样使用
  template: '<span>{{ message }}</span>'
})
---------------------------------
# 动态prop
<div id="app">
    <div>
      <input v-model="parentMsg">
      <br>
      <child v-bind:message="parentMsg"></child>
    </div>
</div>
<script>
// 注册
Vue.component('child', {
  // 声明 props
  props: ['message'],
  // 同样也可以在 vm 实例中像 "this.message" 这样使用
  template: '<span>{{ message }}</span>'
})
// 创建根实例
new Vue({
  el: '#app',
  data: {
    parentMsg: '父组件内容'
  }
})
</script>
----------------------------------
自定义事件
使用 $on(eventName) 监听事件
使用 $emit(eventName) 触发事件
# 逻辑就是：对内，我绑定incrementHandler方法，触发函数'increment'，而'increment'方法实际绑定的是父类中的方法，66666
<div id="app">
    <div id="counter-event-example">
      <p>{{ total }}</p>
      <button-counter v-on:increment="incrementTotal"></button-counter>
      <button-counter v-on:increment="incrementTotal"></button-counter>
    </div>
</div>
<script>
Vue.component('button-counter', {
  template: '<button v-on:click="incrementHandler">{{ counter }}</button>',
  data: function () {
    return {
      counter: 0
    }
  },
  methods: {
    incrementHandler: function () {
      this.counter += 1
      this.$emit('increment')
    }
  },
})
new Vue({
  el: '#counter-event-example',
  data: {
    total: 0
  },
  methods: {
    incrementTotal: function () {
      this.total += 1
    }
  }
})
</script>
# # # # # data 必须是一个函数，这样的好处就是每个实例可以维护一份被返回对象的独立的拷贝，如果 data 是一个对象则会影响到其他实例


自定义指令
<div id="app">
    <p>页面载入时，input 元素自动获取焦点：</p>
    <input v-focus>
</div>
<script>
// 注册一个全局自定义指令 v-focus
Vue.directive('focus', {
  // 当绑定元素插入到 DOM 中。
  inserted: function (el) {
    // 聚焦元素
    el.focus()
  }
})
// 创建根实例
new Vue({
  el: '#app'
})
</script>
-----------------------------
局部注册
<div id="app">
  <p>页面载入时，input 元素自动获取焦点：</p>
  <input v-focus>
</div>
<script>
// 创建根实例
new Vue({
  el: '#app',
  directives: {
    // 注册一个局部的自定义指令 v-focus
    focus: {
      // 指令的定义
      inserted: function (el) {
        // 聚焦元素
        el.focus()
      }
    }
  }
})
</script>


钩子函数
bind: 只调用一次，指令第一次绑定到元素时调用，用这个钩子函数可以定义一个在绑定时执行一次的初始化动作。
inserted: 被绑定元素插入父节点时调用（父节点存在即可调用，不必存在于 document 中）。
update: 被绑定元素所在的模板更新时调用，而不论绑定值是否变化。通过比较更新前后的绑定值，可以忽略不必要的模板更新（详细的钩子函数参数见下）。
componentUpdated: 被绑定元素所在模板完成一次更新周期时调用。
unbind: 只调用一次， 指令与元素解绑时调用。


<nav v-bind:class="active" v-on:click.prevent>
在头部就可以加入click.prevent，以防止单机时进行跳转，就是上下跳很烦的那种

"""



"""导航栏
<style>
nav.home .home,
nav.projects .projects,
nav.services .services,
nav.contact .contact{
    background-color:#e35885;
}
</style>
<div id="main">
 
    <!-- 激活的菜单样式为  active 类 -->
    <!-- 为了阻止链接在点击时跳转，我们使用了 "prevent" 修饰符 (preventDefault 的简称)。 -->
 
    <nav v-bind:class="active" v-on:click.prevent>
 
        <!-- 当菜单上的链接被点击时，我们调用了 makeActive 方法, 该方法在 Vue 实例中创建。 -->

        <a href="#" class="home" v-on:click="makeActive('home')">Home</a>
        <a href="#" class="projects" v-on:click="makeActive('projects')">Projects</a>
        <a href="#" class="services" v-on:click="makeActive('services')">Services</a>
        <a href="#" class="contact" v-on:click="makeActive('contact')">Contact</a>
    </nav>
 
     <!-- 以下 "active" 变量会根据当前选中的值来自动变换 -->
 
    <p>您选择了 <b>{{active}} 菜单</b></p>
</div>

<script>
// 创建一个新的 Vue 实例
var demo = new Vue({
    // DOM 元素，挂载视图模型
    el: '#main',

    // 定义属性，并设置初始值
    data: {
        active: 'home'
    },

    // 点击菜单使用的函数
    methods: {
        makeActive: function(item){
            // 模型改变，视图会自动更新
            this.active = item;
        }
    }
});
</script>
"""


"""编辑文本实例
"""


"""订单列表实例
"""


"""搜索页面实例
"""

