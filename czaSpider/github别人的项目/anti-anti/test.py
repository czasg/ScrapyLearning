"""
感觉这是一个非常不错的例子。dropout。
他的实际作用非常简单。随机去除一定比例的数使之为0，然后剩余的值进行 source/(1-rate)
也就是原来的值是10
然后变为 10 / (1 - 0.6) = 2.5，所以里面有40%左右的数据会变为变为2.5，而剩余60%数据会变为0
以前是使用dropout，表示丢弃这么多比例的数据。剩下的使用rate进行
keep_prob=0.4 == rate=0.6
rate=0.6表示要丢掉60%的数据咯
"""
import tensorflow as tf
rate = tf.compat.v1.placeholder(tf.float32)
x = tf.Variable(tf.ones([10, 10]))
y = tf.nn.dropout(x, rate=rate)
sess = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer())
print(sess.run(y, feed_dict = {rate: 0.6}))  # rate = 1 - keep_prob

