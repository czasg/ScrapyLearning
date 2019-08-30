import tensorflow as tf
import numpy as np
# # ---------------------------------------------------------------
# matrix1 = tf.constant([[3,3]])
# matrix2 = tf.constant([[2],[2]])
# product = tf.matmul(matrix1,matrix2)
# sess = tf.compat.v1.Session()
# result = sess.run(product)
# print(result)
# sess.close()
# with tf.compat.v1.Session() as sess:
#     result2 = sess.run(product)
#     print(result2)
# # ---------------------------------------------------------------


"""
在 Tensorflow 中，定义了某字符串是变量，它才是变量，这一点是与 Python 所不同的。
定义语法： state = tf.Variable()
"""
# state = tf.Variable(1, name='counter')  # 定义变量 state  定了变量，那么初始化变量是最重要的！！
# one = tf.constant(10)  # 定义常量 one
# new_value = tf.add(state, one)  # 定义加法步骤 (注: 此步并没有直接计算)
# update = tf.compat.v1.assign(state, new_value)  # 将 State 更新成 new_value
# init = tf.compat.v1.global_variables_initializer()  # 初始化变量
# with tf.compat.v1.Session() as sess:
#     sess.run(init)
#     for _ in range(3):
#         sess.run(update)
#         print(sess.run(state))  # 注意：直接 print(state) 不起作用！！ 一定要把 sess 的指针指向 state 再进行 print 才能得到想要的结果！


"""
placeholder 是 Tensorflow 中的占位符 暂时储存变量.
Tensorflow 如果想要从外部传入data, 那就需要用到 tf.placeholder(), 然后以这种形式传输数据 sess.run(***, feed_dict={input: **}).
接下来, 传值的工作交给了 sess.run() , 需要传入的值放在了feed_dict={} 并一一对应每一个 input. placeholder 与 feed_dict={} 是绑定在一起出现的
"""
# input1 = tf.compat.v1.placeholder(tf.float32)  #在 Tensorflow 中需要定义 placeholder 的 type ，一般为 float32 形式
# input2 = tf.compat.v1.placeholder(tf.float32)
# ouput = tf.multiply(input1, input2)  # mul = multiply 是将input1和input2 做乘法运算，并输出为 output
# with tf.compat.v1.Session() as sess:
#     print(sess.run(ouput, feed_dict={input1: [7.1], input2: [2.]}))


"""
激励函数y=AF(Wx) 这里的 AF 就是指的激励函数 套在了原函数上 用力一扭, 原来的 Wx 结果就被扭弯了
卷积层中, 推荐的激励函数是 relu. 在循环神经网络中 recurrent neural networks, 推荐的是 tanh 或者是 relu 
激励函数的实质是非线性方程

在 Tensorflow 里定义一个添加层的函数可以很容易的添加神经层,为之后的添加省下不少时间.
神经层里常见的参数通常有weights、biases和激励函数。
然后定义添加神经层的函数def add_layer(),它有四个参数：输入值、输入的大小、输出的大小和激励函数，我们设定默认的激励函数是None。
"""
def add_layer(inputs, in_size, out_size, activation_function=None):
    Weights = tf.Variable(tf.random.normal([in_size, out_size]))  # 随机变量(normal distribution)会比全部为0要好很多，所以我们这里的weights为一个in_size行, out_size列的随机变量矩阵
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)  # biases的推荐值不为0，所以我们这里是在0向量的基础上又加了0.1
    Wx_plus_b = tf.matmul(inputs, Weights) + biases  # 当activation_function——激励函数为None时，输出就是当前的预测值——Wx_plus_b，不为None时，就把Wx_plus_b传到activation_function()函数中得到输出。
    if activation_function is None:
            outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs
# 构建所需的数据。 这里的x_data和y_data并不是严格的一元二次函数的关系，因为我们多加了一个noise,这样看起来会更像真实情况。
x_data = np.linspace(-1,1,300, dtype=np.float32)[:, np.newaxis]
noise = np.random.normal(0, 0.05, x_data.shape).astype(np.float32)
y_data = np.square(x_data) - 0.5 + noise
# 利用占位符定义我们所需的神经网络的输入。 tf.placeholder()就是代表占位符，这里的None代表无论输入有多少都可以，因为输入只有一个特征，所以这里是1。
xs = tf.compat.v1.placeholder(tf.float32, [None, 1])
ys = tf.compat.v1.placeholder(tf.float32, [None, 1])
l1 = add_layer(xs, 1, 10, activation_function=tf.nn.relu)  # 开始定义隐藏层,利用之前的add_layer()函数，这里使用 Tensorflow 自带的激励函数tf.nn.relu。
prediction = add_layer(l1, 10, 1, activation_function=None)  # 接着，定义输出层。此时的输入就是隐藏层的输出——l1，输入有10层（隐藏层的输出层），输出有1层。
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), reduction_indices=[1]))  # 计算预测值prediction和真实值的误差，对二者差的平方求和再取平均。
train_step = tf.compat.v1.train.GradientDescentOptimizer(0.1).minimize(loss)  # 接下来，是很关键的一步，如何让机器学习提升它的准确率。tf.train.GradientDescentOptimizer()中的值通常都小于1，这里取的是0.1，代表以0.1的效率来最小化误差loss
init = tf.compat.v1.global_variables_initializer()
sess = tf.compat.v1.Session()
sess.run(init)
# for i in range(1000):
#     sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
#     if i % 50 == 0:
#         print(sess.run(loss, feed_dict={xs: x_data, ys: y_data}))
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.scatter(x_data, y_data)
plt.ion()
plt.show()
lines = []
for i in range(5000):
    sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
    if i % 50 == 0:
        try:
            ax.lines.remove(lines[0])
        except Exception:
            pass
        prediction_value = sess.run(prediction, feed_dict={xs: x_data})
        lines = ax.plot(x_data, prediction_value, 'r-', lw=5)
        plt.pause(0.1)
