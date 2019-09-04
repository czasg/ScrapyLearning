import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
"""标题：实现一个占位符，创建一个10x10的矩阵，使用dropout和rate分别对其进行处理
###  说明  ###
首先创建两个占位符，每一个占位符需要后期执行run的时候去喂食feed_prob
然后创建一个矩阵，使用tf.ones，该方法和numpy的基本类似嘛
接着定义丢弃率，最后执行定义的丢弃率即可，一次定义，到处使用的意思嘛。记得时候喂食
###  Code  ###
rate = tf.compat.v1.placeholder(tf.float32)
keep_prob = tf.compat.v1.placeholder(tf.float32)
mat = tf.Variable(tf.ones([2, 5]))
dropout_by_keep_prob = tf.nn.dropout(mat, keep_prob=keep_prob)
dropout_by_rate = tf.nn.dropout(mat, rate=rate)
sess = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer())
print(sess.run(dropout_by_keep_prob, feed_dict={keep_prob: 0.6}))
print(sess.run(dropout_by_rate, feed_dict={rate: 0.4}))
"""

"""标题：numpy中关于axis的含义
###  说明  ###
如果单纯从代码的角度看，可以理解为对应list的下标
###  Code  ###
mat = np.array([[[1, 2, 3],[1, 2, 3]], [[1, 2, 3],[1, 2, 3]]])
print(mat)
print(mat.shape)
print(np.mean(mat, axis=0).shape)
print(np.mean(mat, axis=1).shape)
print(np.mean(mat, axis=2).shape)
print(np.mean(mat, axis=-1).shape)
"""

"""标题：神经网络
###  说明  ###
获取数据集，这种数据集的格式和类型，也就是输入和输出一定需要定义好，不然后续会很烦
定义两个占位符，xs和ys分别表示输入和输出，并规定好了，输入为28*28的矩阵，输出为一个长度为10的向量
这里我们还额外定义了两个函数，一个表示添加神经层，一个表示对数据的精确度进行计算
首先，添加神经层函数，他的输入是我们刚刚定义的28*28向量，也就是一行，输出则是一个(1, 10)的二维向量了。这里的激活函数用了softmax
在这里我们就定义了一层神经网络，就直接输出结果进行比对了
然后就是校正误差。loss用了一个看不懂的方程=0=，直接丢到梯度下降里面去了。每次我们只需要执行train_step就可以获取对应的误差数据
我们获取到的数据就是(100, 784)，输出是(100, 10)，train_step是需要投食的，他的xs和ys是占位符。这次喂食只是为了让这个流程能够走通一次，不是特意的针对哪里
还有一个检测的函数，这里使用的prediction，说明是和train_step分开的，后者用于训练流程，实际的预测结果还是要检测前者
检测是头目目标的矩阵，然后输出预测矩阵，与实际结果进行比对，获取精确度
###  Code  ###
def add_layer(inputs, in_size, out_size, activation_func=None):
    weights = tf.Variable(tf.random.normal([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    wx_plus_b = tf.matmul(inputs, weights) + biases
    return activation_func(wx_plus_b) if activation_func else wx_plus_b
def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs})
    correct_prediction = tf.equal(tf.argmax(y_pre, 1), tf.argmax(v_ys, 1))  # tf.argmax获取最大值的索引
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))  # tf.cast 转化数据类型为float32
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys})
    return result
xs = tf.compat.v1.placeholder(tf.float32, [None, 784])  # 28*28
ys = tf.compat.v1.placeholder(tf.float32, [None, 10])
prediction = add_layer(xs, 784, 10, activation_func=tf.nn.softmax)
loss = tf.reduce_mean(-tf.reduce_sum(ys * tf.math.log(prediction), reduction_indices=[1]))
train_step = tf.compat.v1.train.GradientDescentOptimizer(0.5).minimize(loss)
sess = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer())
for i in range(1000):
    # batch_x (100, 784)
    # batch_y (100, 10)
    batch_x, batch_y = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={xs: batch_x, ys: batch_y})
    if i % 50 == 0:
        print(compute_accuracy(mnist.test.images, mnist.test.labels))
"""

"""标题：卷积神经网络
输入输出搞不动，曹乐
"""
def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs, keep_prob: 1})
    correct_prediction = tf.equal(tf.argmax(y_pre, 1), tf.argmax(v_ys, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys, keep_prob: 1})
    return result
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)
def conv2d(x, w):
    # 第一次：(?, 28, 28, 1)  (5, 5, 1, 32)
    # 第二次：(?, 14, 14, 32) (5, 5, 32, 64)
    return tf.nn.conv2d(x, w, strides=[1, 1, 1, 1], padding='SAME')
def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
xs = tf.compat.v1.placeholder(tf.float32, [None, 784]) / 255.
ys = tf.compat.v1.placeholder(tf.float32, [None, 10])
keep_prob = tf.compat.v1.placeholder(tf.float32)
drop_rate = tf.compat.v1.placeholder(tf.float32)
x_image = tf.reshape(xs, [-1, 28, 28, 1])  # 将以为向量转化为目标矩阵

w_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])
h_conv1 = tf.nn.relu(conv2d(x_image, w_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

w_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

w_fc1 = weight_variable([7*7*64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1) + b_fc1)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

w_fc2 = weight_variable([1024, 10])  # 输入是1024，最后的输出是10个
b_fc2 = bias_variable([10])
# h_fc1_drop (?, 1024)
# w_fc2 (1024, 10)
# b_fc2 (10, )
print()
prediction = tf.nn.softmax(tf.matmul(h_fc1_drop, w_fc2) + b_fc2)
loss = tf.reduce_mean(-tf.reduce_sum(ys * tf.math.log(prediction), reduction_indices=[1]))
train_step = tf.compat.v1.train.AdamOptimizer(1e-4).minimize(loss)

sess = tf.compat.v1.Session()
sess.run(tf.global_variables_initializer())

for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    # batch_xs (100, 784)
    # batch_ys (100, 10)
    sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys, keep_prob: 0.5})
    if i % 50 == 0:
        print(compute_accuracy(mnist.test.images[:1000], mnist.test.labels[:1000]))
