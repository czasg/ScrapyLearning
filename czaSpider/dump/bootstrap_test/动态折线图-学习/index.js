// don't try to learn anything from the code, it's a
// series of hacks. this one's all about the visuals.
// - @hakimel

//输入为: { data: [] }
var LineChart = function( options ) {

    var data = options.data; // []
    //console.log(data) 这里确实传进来的是空
    var canvas = document.body.appendChild( document.createElement( 'canvas' ) );  //创建元素并在body中添加
    var context = canvas.getContext( '2d' ); // canvas对象

    var rendering = false,
        paddingX = 40,
        paddingY = 40,
        width = options.width || window.innerWidth, // 当前window的宽度574
        height = options.height || window.innerHeight,  // 当前window的高度604
        progress = 0;

    canvas.width = width;  // 画布的宽高填充整个屏幕
    canvas.height = height;

    var maxValue,
        minValue;

    var y1 = paddingY + ( 0.05 * ( height - ( paddingY * 2 ) ) ), // 66.2  // 这三个坐标是根据当前显示器，计算出三个平分线的Y轴坐标
        y2 = paddingY + ( 0.50 * ( height - ( paddingY * 2 ) ) ), // 302
        y3 = paddingY + ( 0.95 * ( height - ( paddingY * 2 ) ) ); // 537

    format();
    render();

    function format( force ) {  // 定义坐标，定义速度

        maxValue = 0;
        minValue = Number.MAX_VALUE;

        data.forEach( function( point, i ) { //forEach有三个参数，第一个是遍历数组的内容，第二个是数组索引，第三个是数组本身
            maxValue = Math.max( maxValue, point.value );
            minValue = Math.min( minValue, point.value );
        });  // 选出当前数组中的最大值和最小值

        data.forEach( function( point, i ) { // 计算数组中各个标签的坐标位置，x是从做到右逐渐变大，y则与value有灌
            point.targetX = paddingX + ( i / ( data.length - 1 ) ) * ( width - ( paddingX * 2 ) );  // 根据数组的长度平分x轴
            point.targetY = paddingY + ( ( point.value - minValue ) / ( maxValue - minValue ) * ( height - ( paddingY * 2 ) ) );  // 根据最大最小值平分y轴
            point.targetY = height - point.targetY;  // 取反

            if( force || ( !point.x && !point.y ) ) {
                point.x = point.targetX + 30;  // 计算具体的坐标，x需要偏移30  // target是目标x，也就是最后的位置，而这里得到的x是其实位置，我们需要从其实位置移动到目标位置就ok
                point.y = point.targetY;
                point.speed = 0.1//0.04 + ( 1 - ( i / data.length ) ) * 0.05;  // 定义速度吗， 越到后面越慢 // speed就是移动过去的速度，他是位进
            }  // 我定义了速度，怎么起作用呢？还不是速度啊  0.1就可以保证最后一定可以到
        });
    }
    // console.log(data) 仍然为空

    function render() {

        if( !rendering ) {  // 这儿初始化的是False
            requestAnimationFrame( render );  // 我擦，这就开始递归了?
            return;
        }


        context.font = '10px sans-serif';
        context.clearRect( 0, 0, width, height ); // 清除整个画布

        context.fillStyle = '#222';  // 白色，用于画背景的三条线
        context.fillRect( paddingX, y1, width - ( paddingX * 2 ), 1 ); // 在背景后面有三个矩形，蒙蔽
        context.fillRect( paddingX, y2, width - ( paddingX * 2 ), 1 );
        context.fillRect( paddingX, y3, width - ( paddingX * 2 ), 1 ); // 哦哦，这原来是三根坐标线

        if( options.yAxisLabel ) {
            context.save();
            context.globalAlpha = progress;
            context.translate( paddingX - 15, height - paddingY - 10 );  // 重新映射画布上的 位置
            context.rotate( -Math.PI / 2 );  // 旋转当前绘图
            context.fillStyle = '#fff';
            context.fillText( options.yAxisLabel, 0, 0 );
            context.restore();
        }  // 这段代码并未被执行

        var progressDots = Math.floor( progress * data.length );  // 这是一个点，获取不超过输入值的最大整数
        var progressFragment = ( progress * data.length ) - Math.floor( progress * data.length );

        data.forEach( function( point, i ) {  // 画文本，画点的，应该就这两个做作用
            if( i <= progressDots ) {
//              // 这两个很强大，能够对xy轴进行平滑，缩小， 这里就需要注意，目标x和实际位置x之间的差距，如果把我的好就可以慢慢哦听话，不然可能会出现左右横条的请款，这里不够好，感觉很奇怪，可以优化优化
                point.x += ( point.targetX - point.x ) * point.speed; // x加了30  // x变小了  // 定义了这个，就会往左边进行偏移，很神器也很漂亮的操作
                point.y += ( point.targetY - point.y ) * point.speed; // y 未变化
//console.log(point.x, point.y)
                context.save();  // 保存当前环境的状态
                // 这里开始画 文本， 也就是label
                var wordWidth = context.measureText( point.label ).width;  // 返回包含指定文本宽度的对象，也就是获取对象的宽度
                context.globalAlpha = i === progressDots ? progressFragment : 1;
                context.fillStyle = point.future ? '#aaa' : '#fff';
                context.fillText( point.label, point.x - ( wordWidth / 2 ), height - 18 );

                if( i < progressDots && !point.future ) { // 画点
                    context.beginPath();
                    context.arc( point.x, point.y, 4, 0, Math.PI * 2 ); // 画焦点，也就是那个小粗点
                    context.fillStyle = '#1baee1';
                    context.fill();
                } // 这力是画圆点的
            context.restore();  // 返回之前保存过的路径状态和属性， 保存但没画是把
          }
        });

        context.save();
        context.beginPath();  // 绘画开始，或者重新开始绘画  ctx.stroke(); // 进行绘制
        context.strokeStyle = '#1baee1';  // 定义路径的style
        context.lineWidth = 2; // 定义路径宽度

        var futureStarted = false;

        data.forEach( function( point, i ) {

            if( i <= progressDots ) {

                var px = i === 0 ? data[0].x : data[i-1].x, // 前一个坐标点的下标，若是第一个，则为它本身
                    py = i === 0 ? data[0].y : data[i-1].y;

                var x = point.x,  // 获取当前点的坐标，上面是前一个点的坐标
                    y = point.y;

                if( i === progressDots ) {  // 这个函数很重要，起到平滑移动的作用！
                    x = px + ( ( x - px ) * progressFragment );  // ( x - px )表示无和目标之间的差距，以前一个节点为基底，不停加上来是把
                    y = py + ( ( y - py ) * progressFragment );
                } // 这里是平滑作用，但是速度与他貌似没有关系啊

                if( point.future && !futureStarted ) {  // 这个函数是用来化未来节点的
                    futureStarted = true;

                    context.stroke();  // 进行绘制
                    context.beginPath();
                    context.moveTo( px, py );  // 以前一个节点为起始节点， 就可以造成连接在一起的效果是吧
                    context.strokeStyle = '#aaa';

                    if( typeof context.setLineDash === 'function' ) {
                        context.setLineDash( [2,3] );
                    }
                }

                if( i === 0 ) {
                  context.moveTo( x, y );
                }
                else {
                  context.lineTo( x, y );
                }
            }
        });

        context.stroke();
        context.restore();
        //console.log(progress)
        progress += ( 1 - progress ) * 0.02; // 这里才是控制速度的地方，约到后面长的越慢，开始快一些

        requestAnimationFrame( render ); //这也是一个递归
    }

    this.start = function() {
        rendering = true;
    }
  
    this.stop = function() {
        rendering = false;
        progress = 0;
        format( true );
    }
  
    this.restart = function() {
        this.stop();
        this.start();
    }
  
    this.append = function( points ) {
        progress -= points.length / data.length;
        data = data.concat( points );
        format();
    }
  
    this.populate = function( points ) { //在此处定义了data函数
        progress = 0;
        data = points;
        format();
    }
};

var chart = new LineChart({ data: [] });

reset(); // 该函数就是用来初始化data数值的吗

chart.start();


// 以下为三种操作方法
function append() {
    chart.append([
        { label: 'Rnd', value: 1300 + ( Math.random() * 1500 ), future: true }
    ]);
}



function restart() {
    chart.restart();
}


function reset() { // 定义标签和值， 原来如此，在这里就开始定义不同的折现坐标了，相当牛逼
    chart.populate([
        { label: 'One', value: 0 },
        { label: 'Two', value: 100 },
        { label: 'Three', value: 200 },
        { label: 'Four', value: 840 },
        { label: 'Five', value: 620 },
        { label: 'Six', value: 500 },
        { label: 'Seven', value: 600 },
        { label: 'Eight', value: 1100 },
        { label: 'Nine', value: 800 },
        { label: 'Ten', value: 900 },
        { label: 'Eleven', value: 1200, future: true },
        { label: 'Twelve', value: 1400, future: true }
    ]);
}
