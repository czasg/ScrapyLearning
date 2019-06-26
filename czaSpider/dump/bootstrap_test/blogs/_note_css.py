__FILE__ = "Learn For CSS"

"""
position: 对元素进行定义，absolute是相对父级定位，fixed是相对浏览器定位
top: 相对于父级来说，头相隔距离
bottom: 相对于父级来说，地步相隔距离
left： 相对左边缘来说，偏移距离
z-index: 将一个元素置于另一个元素之上，数值越大，优先级越大
display: 显示属性，默认为inline，block为显示块级元素
padding: 设置内边距，四个数值分别对应上右下左
overflow-x: 是否对内容的左/右边缘进行裁剪
->设置为visible，不裁剪，可能会出现在显示框之外
->设置为hidden，裁剪内容不提供滚动机制
->设置为scroll，裁剪内容并提供滚动机制，上下左右都提供
->设置为auto，若溢出则提供滚动机制 - 推荐使用auto -
->设置为
->设置为
overflow-y: 是否对内容的上/下边缘进行裁剪
border-right: 设置右边框样式。dotted点状、solid实线、double双线、dashed虚线
@media: 当文档达到某些条件是触发。min-width:768px则表示当宽度大于167时触发

line-height: 属性设置行间的距离（行高） .li 就表示被一个li之间的行间距是这么多
border-style: 设置元素边框的样式，或单独设置边框样式。dotted solid double dashed; 分别表示点状、实线、双线、虚线。
border-width: 设置各边框的宽度
white-space: nowrap 设置段落中的文本不进行换行
transition: width 2s;  -- transition: property duration timing-function delay; 分别表示：需要设置的css属性名称、规定完成过渡需要的时间、规定速度小郭的速度曲线、定义过渡时间合适开始

label:before{ // 在标签前面添加元素
content: '在标签前面添加内容'
background-repeat: repeat；  // 是否重复，这个就是去全部重复啊 infinite 无限重复无限滚动概念
}
"""