// CLASSES
class Shard {
    constructor(x, y, hue) {
        this.x = x;
        this.y = y;
        this.hue = hue;  // Math.floor(Math.random() * 360)  可以爆炸出财社的礼花
        this.lightness = 50;
        this.size = 15 + Math.random() * 10;  // 这个是爆炸后碎片的半径
        const angle = Math.random() * 2 * Math.PI;  // 这个角度是碎片的角度
        const blastSpeed = 1 + Math.random() * 6;
        this.xSpeed = Math.cos(angle) * blastSpeed;
        this.ySpeed = Math.sin(angle) * blastSpeed;
        this.target = getTarget();
        this.ttl = 100;
        this.timer = 0;
    }
    draw() {
        ctx2.fillStyle = `hsl(${this.hue}, 100%, ${this.lightness}%)`;
        ctx2.beginPath(); // 调用beginPath和closePath，就是为了填充这个圆吗 -- 不对
        ctx2.arc(this.x, this.y, this.size, 0, 2 * Math.PI);  // 画圆，也就是爆炸碎片
        ctx2.closePath();
        ctx2.fill();  // 针对每一个碎片对象，画一个圆出来咯
    }
    update() {
        if (this.target) {
            const dx = this.target.x - this.x;  // 起始与目的地之间的差距，早x轴上
            const dy = this.target.y - this.y;
            const dist = Math.sqrt(dx * dx + dy * dy);  // 两点之间的直线距离
            const a = Math.atan2(dy, dx);  // 计算角度
            const tx = Math.cos(a) * 5;
            const ty = Math.sin(a) * 5;
            this.size = lerp(this.size, 2.5, 0.05);  // 牛逼，控制碎片的大小变化

            if (dist < 5) {
                this.lightness = lerp(this.lightness, 100, 0.01);
                this.xSpeed = this.ySpeed = 0;
                this.x = lerp(this.x, this.target.x + fidelity / 2, 0.05);
                this.y = lerp(this.y, this.target.y + fidelity / 2, 0.05);
                this.timer += 1;
            } else if (dist < 10) {
                this.lightness = lerp(this.lightness, 100, 0.01);
                this.xSpeed = lerp(this.xSpeed, tx, 0.1);
                this.ySpeed = lerp(this.ySpeed, ty, 0.1);
                this.timer += 1;
            } else {
                this.xSpeed = lerp(this.xSpeed, tx, 0.02);
                this.ySpeed = lerp(this.ySpeed, ty, 0.02);
            }
        } else {
            this.ySpeed += 0.05;
            //this.xSpeed = lerp(this.xSpeed, 0, 0.1);
            this.size = lerp(this.size, 1, 0.05);

            if (this.y > c2.height) {
                shards.forEach((shard, idx) => {
                    if (shard === this) {
                        shards.splice(idx, 1);
                    }
                });
            }
        }
        this.x = this.x + this.xSpeed;
        this.y = this.y + this.ySpeed;
    }
}


class Rocket {
    constructor() {
        const quarterW = c2.width / 4;  // 四分之一的屏宽
        this.x = quarterW + Math.random() * (c2.width - quarterW);  // 火箭出现的位置，x轴，位置随机
        this.y = c2.height - 15;  // 火箭出来的位子，高度，高度固定
        this.angle = Math.random() * Math.PI / 4 - Math.PI / 6; // 方向，出现的角度  10*Math.PI/180 ， 这列写90度就会直接炸， 90度就是水平的意思， 0就是垂直向上
        this.blastSpeed = 6 + Math.random() * 7;  // 火箭出现的速度
        this.shardCount = 15 + Math.floor(Math.random() * 15);
        this.xSpeed = Math.sin(this.angle) * this.blastSpeed;
        this.ySpeed = -Math.cos(this.angle) * this.blastSpeed;
        this.hue = Math.floor(Math.random() * 360); // 火箭出现的颜色。每一个火箭都是一个Rocket对象
        this.trail = [];
    }
    draw() {
        ctx2.save();
        ctx2.translate(this.x, this.y);  // translate() 方法重新映射画布上的 (0,0) 位置。相当于移动下标的意思
        ctx2.rotate(Math.atan2(this.ySpeed, this.xSpeed) + Math.PI / 2);  // 根据xy轴的速度，计算角度，牛逼  //  + Math.PI / 2 后面这段也非常重要，因为射出去的是一个矩阵，所以需要再旋转90度
        ctx2.fillStyle = `hsl(${this.hue}, 100%, 50%)`;
        ctx2.fillRect(0, 0, 5, 15);
        ctx2.restore();
//        console.log(Math.atan2(this.ySpeed, this.xSpeed), this.y)
    }
    update() {
        this.x = this.x + this.xSpeed;  // 更新x轴的下一个位置，更新y轴的下一个位置，而且y轴的位置是递增的？
        this.y = this.y + this.ySpeed;
        this.ySpeed += 0.1;  // 若果把这行注释掉，那么火箭就永远是直线运动，一直上天不会下来，我给了他一个y轴上的增量， 原来如此，y轴上的速度，是用来计算角度的，当y逐渐增大的时候，
    } // 原来如此，y轴上的速度是一个负值，相对坐标系的问题，当一个负值+上0.1后值是变小的

    explode() {
        for (let i = 0; i < 30; i++) {  // 达到爆炸条件，则开始创建碎片对象，这列可以设置数量，都以最后爆炸点初始化，继承颜色
            shards.push(new Shard(this.x, this.y, this.hue));
        }
    }
}


// INITIALIZATION
const [c1, c2, c3] = document.querySelectorAll('canvas');  // 找到三个canvas对象
const [ctx1, ctx2, ctx3] = [c1, c2, c3].map(c => c.getContext('2d'));  // 对这三个对象进行获取画图属性
let fontSize = 200;  // 初始化字体200
const rockets = [];  // 火箭 - 这是装的什么
const shards = [];  // 碎片 - 这是装的什么
const targets = [];  // 目标 - 这里是？
const fidelity = 3;  // 保真度，是3  // 绘画中间字体的时候，每次填写的方位， 他是由矩阵拼接起来的，所以定义矩阵的长宽很重要
let counter = 0;  // 计数
c2.width = c3.width = window.innerWidth;  // 初始化第二、三DOM的宽度和高度
c2.height = c3.height = window.innerHeight;  // 这是直接操作的DON了，不是画布
ctx1.fillStyle = '#000';  // 这是画布
const text = 'IOCO';  // 这里是重要的入口，定义文本
let textWidth = 99999999;  // 文本宽度？

while (textWidth > window.innerWidth) { // 这毫无疑问是true
    ctx1.font = `900 ${fontSize--}px Arial`;  // 画布1的字体大小是200
    textWidth = ctx1.measureText(text).width; // 重新定义宽度，为文本宽度
//  console.log(textWidth)
}
// 画布1也是字体，但是他的字体是用来做圆料的，用来提供target，真正实现字体的是画布3
c1.width = textWidth;  // 又操作DOM，定义其宽度为文本的宽度
c1.height = fontSize * 1.5;  // 高度为字体宽度的1.5倍
ctx1.font = `900 ${fontSize}px Arial`; // 这个时候变成了199把
ctx1.fillText(text, 0, fontSize);
const imgData = ctx1.getImageData(0, 0, c1.width, c1.height);  // 复制画布上指定矩形的像素数据
for (let i = 0, max = imgData.data.length; i < max; i += 4) {
    const alpha = imgData.data[i + 3];
    const x = Math.floor(i / 4) % imgData.width;
    const y = Math.floor(i / 4 / imgData.width);
//    console.log({x,y})  // 创一个矩阵，x是从9到381，而y是x满后进1
    if (alpha && x % fidelity === 0 && y % fidelity === 0) { // 灰度值大于0，且坐标为3的倍数
        targets.push({ x, y });  // 把像素推到目标队列里面去
    }  // 如果全部不要，则会维护一个整个画布1，不要alpha也是整个画布1，
} // 不加后面的过滤，太多target了

ctx3.fillStyle = '#aaa';  // 画布三，是装的字体，aaa拜师紫色，而fff表示白色
ctx3.shadowColor = '#FFF';
ctx3.shadowBlur = 25;

// ANIMATION LOOP
(function loop() {
    // 这里的画布二是背景颜色
    // 255,252,153,0.5  暖黄色
    // 144, 238 ,144, 0.5  半透明青苹果色
    ctx2.fillStyle = "rgba(255,252,153,0.5)";  // 0, 0, 0, .1 完全不透明的黑色
    ctx2.fillRect(0, 0, c2.width, c2.height);
    //ctx2.clearRect(0, 0, c2.width, c2.height);
    counter += 1;

    if (counter % 15 === 0) {  // 这个是用来过滤火箭的，不然太多了吓人啊
        rockets.push(new Rocket());  // 说明这个火箭还是真弹出去的火箭
    }
    rockets.forEach((r, i) => {
        r.draw();
        r.update();
        if (r.ySpeed > 0) {  // 是否爆炸
            r.explode();
            rockets.splice(i, 1); // 删除该火箭？
        }
    });

    shards.forEach((s, i) => {
        s.draw();
        s.update();

        if (s.timer >= s.ttl || s.lightness >= 99) {
            ctx3.fillRect(s.target.x, s.target.y, fidelity + 1, fidelity + 1);
            shards.splice(i, 1);
        }
    });

    requestAnimationFrame(loop);
})();

// HELPER FUNCTIONS
const lerp = (a, b, t) => Math.abs(b - a) > 0.1 ? a + t * (b - a) : b;  // ab相差是否大于0.1， 不是的话就取吧，否则就要经过一番计算
//(this.size, 1.5, 0.05)

function getTarget() {  // 从target数组中随机去一个，并删除，将此值作为target值传给对象
    if (targets.length > 0) {
//        console.log(targets.length)
        const idx = Math.floor(Math.random() * targets.length);
//        console.log(targets.length, idx)
        let { x, y } = targets[idx];
        targets.splice(idx, 1);

        x += c2.width / 2 - textWidth / 2;  // 原来是画布位置放的不是最后位置，需要微调下
        y += c2.height / 2 - fontSize / 2;  // 这两个的作用将他放在正中央

        return { x, y };
    }
}