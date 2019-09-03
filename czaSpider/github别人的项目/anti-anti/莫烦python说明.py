__file__ = 'note'
import tensorflow as tf

"""
分类和回归问题：
主要区别在于输出变量的类型上。
定量输出的是回归，或者说是连续变量预测。 如预测房价是一个回归任务
定性输出是分类，或者说是离散变量预测。把东西分为几类，比如猪狗，就是一个分类任务。

"""
# from  tensorflow.examples.tutorials.mnist import input_data
# def add_layer(inputs, in_size, out_size, activation_function=None):
#     Weights = tf.Variable(tf.random_normal([in_size, out_size]))
#     biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
#     Wx_plus_b = tf.matmul(inputs, Weights) + biases
#     if activation_function is None:
#         outputs = Wx_plus_b
#     else:
#         outputs = activation_function(Wx_plus_b)
#     return outputs
# def compute_accuracy(v_xs, v_ys):
#     global prediction
#     y_pre = sess.run(prediction, feed_dict={xs: v_xs})
#     correct_prediction = tf.equal(tf.argmax(y_pre,1), tf.argmax(v_ys,1))
#     accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
#     result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys})
#     return result
# mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
# xs = tf.placeholder(tf.float32, [None, 784]) # 28x28 - 每张图片的分辨率是28×28
# ys = tf.placeholder(tf.float32, [None, 10])  # 输出是数字0到9，共10类。
# prediction = add_layer(xs, 784, 10, activation_function=tf.nn.softmax)  # 输入层有784，输出只有10层 其中输入数据是784个特征，输出数据是10个特征，激励采用softmax函数
# # todo loss函数（即最优化目标函数）选用交叉熵函数。交叉熵用来衡量预测值和真实值的相似程度，如果完全相同，它们的交叉熵等于零。
# # todo 熵值越小，越趋近于稳定。这是描述混乱程度的意思咯。
# cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),reduction_indices=[1])) # loss  最优化目标函数
# # todo train方法（最优化算法）采用梯度下降法。
# train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
# sess = tf.Session()
# sess.run(tf.global_variables_initializer())
# for i in range(1000):
#     batch_xs, batch_ys = mnist.train.next_batch(100)
#     sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys})
#     if i % 50 == 0:
#         print(compute_accuracy(mnist.test.images, mnist.test.labels))

"""
针对过拟合，
首先可以采用增大训练数据量的方式，将过拟合曲线慢慢拉直。
其次我呢吧可以采用正规化的方法。如：
我们简化机器学习的关键公式为 y=Wx，W为机器需要学习到的各种参数.在过拟合中, W 的值往往变化得特别大或特别小.为了不让W变化太大, 我们在计算误差上做些手脚
始的 cost 误差是这样计算，cost = 预测值-真实值的平方 。如果 W 变得太大, 我们就让 cost 也跟着变大，变成一种惩罚机制.所以我们把 W 自己考虑进来
这里 abs 是绝对值. 这一种形式的 正规化 叫做 l1 正规化
L2 正规化和 l1 类似, 只是绝对值换成了平方. 其他的l3, l4 也都是换成了立方和4次方等等
还有一种专门用在神经网络的正规化的方法, 叫作 dropout
在训练的时候, 我们随机忽略掉一些神经元和神经联结 , 使得这个神经网络变得”不完整”。到第二次再随机忽略另一些, 变成另一个不完整的神经网络
有了这些随机 drop 掉的规则
我们都让每一次预测结果都不会依赖于其中某部分特定的神经元.
像l1, l2正规化一样, 过度依赖的 W , 也就是训练参数的数值会很大, l1, l2会惩罚这些大的 参数. Dropout 的做法是从根本上让神经网络没机会过度依赖.

当keep_prob=1时，模型对训练数据的适应性优于测试数据，存在overfitting，输出如下： 红线是 train 的误差, 蓝线是 test 的误差.
"""
# from sklearn.datasets import load_digits
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelBinarizer
# digits = load_digits()  # 准备数据
# X = digits.data
# y = digits.target
# y = LabelBinarizer().fit_transform(y)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)  # 其中X_train是训练数据, X_test是测试数据。
# def add_layer(inputs, in_size, out_size, layer_name, activation_function=None, ):
#     Weights = tf.Variable(tf.random_normal([in_size, out_size]))
#     biases = tf.Variable(tf.zeros([1, out_size]) + 0.1, )
#     # tf.multiply（）两个矩阵中对应元素各自相乘
#     # tf.matmul（）将矩阵a乘以矩阵b，生成a * b。
#     Wx_plus_b = tf.matmul(inputs, Weights) + biases
#     # 在不同的训练过程中随机扔掉一部分神经元
#     # 也就是让某个神经元的激活值以一定的概率p，让其停止工作，这次训练过程中不更新权值，也不参加神经网络的计算
#     # 但是它的权重得保留下来（只是暂时不更新而已），因为下次样本输入时它可能又得工作了
#     # x，你自己的训练、测试数据等  keep_prob，dropout概率
#     # 输出的非0元素是原来的 “1/keep_prob” 倍
#     # 输入和输出的tensor的shape果然是一样的
#     # 不是0的元素都变成了原来的 “1/keep_prob” 倍
#     # 使输入tensor中某些元素变为0，其它没变0的元素变为原来的1/keep_prob大小！
#     Wx_plus_b = tf.nn.dropout(Wx_plus_b, keep_prob)
#     if activation_function is None:
#         outputs = Wx_plus_b
#     else:
#         outputs = activation_function(Wx_plus_b, )
#     tf.summary.histogram(layer_name + '/outputs', outputs)  # 用来显示直方图信息，其格式为
#     return outputs
# # define placeholder for inputs to network
# # 它作为一个placeholder，在run时传入， 当keep_prob=1的时候，相当于100%保留，也就是dropout没有起作用。
# keep_prob = tf.placeholder(tf.float32)  # keep_prob是保留概率 即我们要保留的结果所占比例
# xs = tf.placeholder(tf.float32, [None, 64])  # 8x8 64是指的数据的尺寸，None指的batch size的大小，所以可以是任何数。
# ys = tf.placeholder(tf.float32, [None, 10])  #
# # 添加隐含层和输出层, 64输入层，50个输出层。最后是50个输入，10个输出
# l1 = add_layer(xs, 64, 50, 'l1', activation_function=tf.nn.tanh)
# prediction = add_layer(l1, 50, 10, 'l2', activation_function=tf.nn.softmax)
# # 交叉熵用来衡量预测值和真实值的相似程度，如果完全相同，交叉熵就等于零。
# cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction), reduction_indices=[1]))  # loss
# tf.summary.scalar('loss', cross_entropy)  # 用来显示标量信息 一般在画loss,accuary时会用到这个函数
# train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)  # train方法（最优化算法）采用梯度下降法。
# sess = tf.Session()
# merged = tf.summary.merge_all()  # merge_all 可以将所有summary全部保存到磁盘，以便tensorboard显示  tf.summary()能够保存训练过程以及参数分布图并在tensorboard显示。
# # summary writer goes in here
# train_writer = tf.summary.FileWriter("logs/train", sess.graph)  # 指定一个文件用来保存图。
# test_writer = tf.summary.FileWriter("logs/test", sess.graph)
# sess.run(tf.global_variables_initializer())
# for i in range(500):
#     # here to determine the keeping probability
#     sess.run(train_step, feed_dict={xs: X_train, ys: y_train, keep_prob: 0.5})
#     if i % 50 == 0:
#         # record loss
#         train_result = sess.run(merged, feed_dict={xs: X_train, ys: y_train, keep_prob: 1})
#         test_result = sess.run(merged, feed_dict={xs: X_test, ys: y_test, keep_prob: 1})
#         train_writer.add_summary(train_result, i)
#         test_writer.add_summary(test_result, i)  # 调用其add_summary（）方法将训练过程数据保存在filewriter指定的文件中

"""
卷积神经网络(图像和语音识别)
神经网络是由一连串的神经层组成,每一层神经层里面有存在有很多的神经元 每一种神经网络都会有输入输出值 当输入值是图片的时候, 实际上输入神经网络的并不是那些色彩缤纷的图案,而是一堆堆的数字.
卷积：卷积也就是说神经网络不再是对每个像素的输入信息做处理了,而是图片上每一小块像素区域进行处理 ， 这种做法加强了图片信息的连续性. 使得神经网络能看到图形, 而非一个点
具体来说, 卷积神经网络有一个批量过滤器, 持续不断的在图片上滚动收集图片里的信息,每一次收集的时候都只是收集一小块像素区域, 然后把收集来的信息进行整理, 这时候整理出来的信息有了一些实际上的呈现,
然后在以同样的步骤, 用类似的批量过滤器扫过产生的这些边缘信息, 神经网络从这些边缘信息里面总结出更高层的信息结构,比如说总结的边缘能够画出眼睛,鼻子等等. 
再经过一次过滤, 脸部的信息也从这些眼睛鼻子的信息中被总结出来. 最后我们再把这些信息套入几层普通的全连接神经层进行分类, 这样就能得到输入的图片能被分为哪一类的结果了.
图片有长, 宽, 高 三个参数   黑白照片的话, 高的单位就只有1, 彩色照片, 高度为3
以彩色照片为例子. 过滤器就是影像中不断移动的东西, 他不断在图片收集小批小批的像素块, 收集完所有信息后, 输出的值
我们可以理解输出成是一个高度更高,长和宽更小的”图片”. 这个图片里就能包含一些边缘信息
然后以同样的步骤再进行多次卷积, 将图片的长宽再压缩, 高度再增加, 就有了对输入图片更深的理解. 
将压缩,增高的信息嵌套在普通的分类神经层上,我们就能对这种图片进行分类了.
池化：
每一次卷积的时候, 神经层可能会无意地丢失一些信息.
池化 (pooling) 就可以很好地解决这一问题. 而且池化是一个筛选过滤的过程, 能将 layer 中有用的信息筛选出来, 给下一个层分析 同时也减轻了神经网络的计算负担
也就是说在卷集的时候, 我们不压缩长宽, 尽量地保留更多信息
压缩的工作就交给池化了,这样的一项附加工作能够很有效的提高准确性
也就是池化将整个流程划分为了两步，第一步扫描出信息，增加高度。然后再压缩长宽。而不是一次进行到位
从下到上的顺序,首先是输入的图片(image), 经过一层卷积层 (convolution), 然后在用池化(pooling)方式处理卷积的信息 然后在经过一次同样的处理, 把得到的第二次处理的信息传入两层全连接的神经层 (fully connected)

卷积神经网络包含输入层、隐藏层和输出层，隐藏层又包含卷积层和pooling层，
图像输入到卷积神经网络后通过卷积来不断的提取特征
每提取一个特征就会增加一个feature map
所以会看到视频教程中的立方体不断的增加厚度，那么为什么厚度增加了但是却越来越瘦了呢，
这就是pooling层的作用喽，pooling层也就是下采样，通常采用的是最大值pooling和平均值pooling
因为参数太多喽，所以通过pooling来稀疏参数，使我们的网络不至于太复杂
Convolutional 卷积 - 提取特征
pooling 池化 - 下采样层

convolutional layer1 + max pooling;
convolutional layer2 + max pooling;
fully connected layer1 + dropout;
fully connected layer2 to prediction.
"""
# from tensorflow.examples.tutorials.mnist import input_data
# mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
#
# def compute_accuracy(v_xs, v_ys):
#     global prediction
#     y_pre = sess.run(prediction, feed_dict={xs: v_xs, keep_prob: 1})
#     correct_prediction = tf.equal(tf.argmax(y_pre,1), tf.argmax(v_ys,1))
#     accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
#     result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys, keep_prob: 1})
#     return result
# # 定义Weight变量，输入shape，返回变量的参数
# def weight_variable(shape):
#     initial = tf.truncated_normal(shape, stddev=0.1)  # 产生随机变量来进行初始化
#     return tf.Variable(initial)
# # 定义biase变量
# def bias_variable(shape):
#     initial = tf.constant(0.1, shape=shape)
#     return tf.Variable(initial)
# # conv2d 二维的卷积函数，x是图片的所有参数，W是此卷积层的权重
# def conv2d(x, W):  # 定义步长strides=[1,1,1,1]，strides[0]和strides[3]的两个1是默认值
#     return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')  # 中间两个1代表padding时在x方向运动一步，y方向运动一步。padding采用的方式是SAME
# # 定义池化pooling。为了得到更多的图片信息，padding时我们选的是一次一步
# # # 也就是strides[1]=strides[2]=1。这样得到的图片尺寸没有变化
# # # 而我们希望压缩一下图片，也就是参数能少一些从而减小系统的复杂度，因此我们采用pooling来稀疏化参数。也就是卷积神经网络中所谓的下采样层
# # # pooling 有两种，一种是最大值池化，一种是平均值池化
# def max_pool_2x2(x):
#     return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')  # 最大值池化
# # 定义一下输入的placeholder
# xs = tf.placeholder(tf.float32, [None, 784])/255.   # 28x28
# ys = tf.placeholder(tf.float32, [None, 10])
# keep_prob = tf.placeholder(tf.float32)  # 解决过拟合
# # 处理我们的xs，把xs的形状变成[-1,28,28,1]，-1代表先不考虑输入的图片例子多少这个维度，后面的1是channel的数量，RGB图像，那么channel就是3
# x_image = tf.reshape(xs, [-1, 28, 28, 1])
# ## conv1 layer ##
# # 先定义本层的Weight,卷积核patch的大小是5x5，又因为黑白图片channel是1所以输入是1，输出是32个featuremap
# W_conv1 = weight_variable([5,5, 1,32]) # patch 5x5, in size 1, out size 32
# b_conv1 = bias_variable([32])  # 接着定义bias。大小是32个长度，因此我们传入它的shape为[32]
# # 定义好了Weight和bias，我们就可以定义卷积神经网络的第一个卷积层h_conv1=conv2d(x_image,W_conv1)+b_conv1
# # 同时我们对h_conv1进行非线性处理，也就是激活函数来处理。这里我们用的是tf.nn.relu（修正线性单元）来处理
# # 要注意的是，因为采用了SAME的padding方式，输出图片的大小没有变化依然是28x28，只是厚度变厚了，因此现在的输出大小就变成了28x28x32
# h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1) # output size 28x28x32 tf.nn.relu是激活函数
# # 最后我们再进行pooling的处理就ok啦， 经过pooling的处理，输出大小就变为了14x14x32
# h_pool1 = max_pool_2x2(h_conv1)                                         # output size 14x14x32
# ## conv2 layer ## 定义第二层卷积。输入就是上一层的输出 本层我们的卷积核patch的大小是5x5，有32个featuremap所以输入就是32，输出呢我们定为64
# W_conv2 = weight_variable([5,5, 32, 64]) # patch 5x5, in size 32, out size 64
# b_conv2 = bias_variable([64])
# h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2) # output size 14x14x64  第二个卷积层
# h_pool2 = max_pool_2x2(h_conv2)                          # output size 7x7x64  pooling处理
# ## fc1 layer ##  建立全连接层
# W_fc1 = weight_variable([7*7*64, 1024])  # 此时weight_variable的shape输入就是第二个卷积层展平了的输出大小: 7x7x64
# b_fc1 = bias_variable([1024])  # 后面的输出size我们继续扩大，定为1024
# # [n_samples, 7, 7, 64] ->> [n_samples, 7*7*64]
# # 通过tf.reshape()将h_pool2的输出值从一个三维的变为一维的数据，-1表示先不考虑输入图片例子维度, 将上一个输出结果展平
# h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
# h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)  # 然后将展平后的h_pool2_flat与本层的W_fc1相乘（注意这个时候不是卷积了）
# h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)  # 考虑过拟合问题，加一个dropout的处理
# ## fc2 layer ##
# W_fc2 = weight_variable([1024, 10])  # 输入是1024，最后的输出是10个
# b_fc2 = bias_variable([10])
# prediction = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)  # prediction就是我们最后的预测值。用softmax分类器（多分类，输出是各个类的概率）,对我们的输出进行分类
# # 利用交叉熵损失函数来定义我们的cost function
# cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),
#                                               reduction_indices=[1]))       # loss
# # 用tf.train.AdamOptimizer()作为我们的优化器进行优化，使我们的cross_entropy最小
# train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
#
# sess = tf.Session()
# sess.run(tf.global_variables_initializer())
#
# for i in range(1000):
#     batch_xs, batch_ys = mnist.train.next_batch(100)
#     sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys, keep_prob: 0.5})
#     if i % 50 == 0:
#         print(compute_accuracy(
#             mnist.test.images[:1000], mnist.test.labels[:1000]))

"""
数据保存于提取
"""
## 保存 ##
# W_save = tf.Variable([[1,2,3],[3,4,5]], dtype=tf.float32, name='weights')
# b_save = tf.Variable([[1,2,3]], dtype=tf.float32, name='biases')
# init = tf.global_variables_initializer()
# saver = tf.train.Saver()
# with tf.Session() as sess:
#     sess.run(init)
#     save_path = saver.save(sess, "my_net/save_net.ckpt")
#     print("Save to path: ", save_path)
## 提取 ##
# import numpy as np
# W_get = tf.Variable(np.arange(6).reshape((2, 3)), dtype=tf.float32, name="weights")  # 建立对应的容器
# b_get = tf.Variable(np.arange(3).reshape((1, 3)), dtype=tf.float32, name="biases")
# saver = tf.train.Saver()
# with tf.Session() as sess:
#     saver.restore(sess, "my_net/save_net.ckpt")
#     print("weights:", sess.run(W_get))
#     print("biases:", sess.run(b_get))