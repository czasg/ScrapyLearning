#coding:utf-8
from gen_captcha import gen_captcha_text_and_image
# from gen_captcha import number
# from gen_captcha import alphabet
# from gen_captcha import ALPHABET

import numpy as np
import tensorflow as tf
number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']

text, image = gen_captcha_text_and_image()
print("验证码图像channel:", image.shape)  # (60, 160, 3) 这里的image是一个numpy.array对象
# 图像大小
IMAGE_HEIGHT = 60
IMAGE_WIDTH =  200  # 160
MAX_CAPTCHA = len(text)  # 字体的个数嘛
print("验证码文本最长字符数", MAX_CAPTCHA)   # 验证码最长4字符; 我全部固定为4,可以不固定. 如果验证码长度小于4，用'_'补齐

# 把彩色图像转为灰度图像（色彩对识别验证码没有什么用）
def convert2gray(img):  # 这段转化为灰度图的代码我是表示怀疑的哦
	if len(img.shape) > 2:
		gray = np.mean(img, -1)  # 对每行求均值，把高度转化为1维的了
		# 上面的转法较快，正规转法如下
		# r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
		# gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
		return gray  # （60, 160）
	else:
		return img

"""
cnn在图像大小是2的倍数时性能最高, 如果你用的图像大小不是2的倍数，可以在图像边缘补无用像素。
np.pad(image【,((2,3),(2,2)), 'constant', constant_values=(255,))  # 在图像上补2行，下补3行，左补2行，右补2行
"""

# 文本转向量
char_set = number + alphabet + ALPHABET + ['_']  # 如果验证码长度小于4, '_'用来补齐
CHAR_SET_LEN = len(char_set)  # 63
print(CHAR_SET_LEN, MAX_CAPTCHA)
# 这段代码的作用就是维护一个所有数据的数组，初始化为1，然后查询是哪一个子串，就在对应的位置转化为1
def text2vec(text):
	text_len = len(text)
	if text_len > MAX_CAPTCHA:
		raise ValueError('验证码最长4个字符')

	vector = np.zeros(MAX_CAPTCHA*CHAR_SET_LEN)  # 4 * 63
	def char2pos(c):
		if c =='_':
			k = 62
			return k
		k = ord(c)-48
		if k > 9:
			k = ord(c) - 55
			if k > 35:
				k = ord(c) - 61
				if k > 61:
					raise ValueError('No Map')
		return k
	for i, c in enumerate(text):  # text就是目标，只有4个把
		idx = i * CHAR_SET_LEN + char2pos(c)  # i * 63 +
		vector[idx] = 1  # 这个转化有点眼熟，对所有维护一个数组，然后匹配待哪一个，就将之设置为1，这个nice呀
	return vector
# 向量转回文本，就是使用二进制码的一种高级用法，速度比我快一些而已，不好理解=0=
def vec2text(vec):
	char_pos = vec.nonzero()[0]
	text=[]
	for i, c in enumerate(char_pos):
		char_at_pos = i #c/63
		char_idx = c % CHAR_SET_LEN
		if char_idx < 10:
			char_code = char_idx + ord('0')
		elif char_idx <36:
			char_code = char_idx - 10 + ord('A')
		elif char_idx < 62:
			char_code = char_idx-  36 + ord('a')
		elif char_idx == 62:
			char_code = ord('_')
		else:
			raise ValueError('error')
		text.append(chr(char_code))
	return "".join(text)

"""
#向量（大小MAX_CAPTCHA*CHAR_SET_LEN）用0,1编码 每63个编码一个字符，这样顺利有，字符也有
vec = text2vec("F5Sd")
text = vec2text(vec)
print(text)  # F5Sd
vec = text2vec("SFd5")
text = vec2text(vec)
print(text)  # SFd5
"""

# 生成一个训练batch
def get_next_batch(batch_size=128):  # 生成128行的意思咯，第一个参数128，后面的居然不一样
    batch_x = np.zeros([batch_size, IMAGE_HEIGHT*IMAGE_WIDTH])  # 60 * 160
    batch_y = np.zeros([batch_size, MAX_CAPTCHA*CHAR_SET_LEN])  # 63 * 4

    # 有时生成图像大小不是(60, 160, 3)
    def wrap_gen_captcha_text_and_image():
        while True:
            text, image = gen_captcha_text_and_image()
            if image.shape == (60, 200, 3):  # (60, 160, 3):
                return text, image

    for i in range(batch_size):  # 每次训练生成128张图片咯，而且这些图片都撞到一个矩阵里面，可以台夸张了把
        text, image = wrap_gen_captcha_text_and_image()
        image = convert2gray(image)  # 转化为灰度图
        # array.flatten() 将矩阵降到一维，这个就厉害了啊
        batch_x[i,:] = image.flatten() / 255 # (image.flatten()-128)/128  mean为0
        # print(text2vec(text).shape)
        batch_y[i,:] = text2vec(text)
    # print(batch_x, batch_y)
    return batch_x, batch_y  # 按这种情况来看，x是图片，y是对应的标签

####################################################################

X = tf.placeholder(tf.float32, [None, IMAGE_HEIGHT*IMAGE_WIDTH])
Y = tf.placeholder(tf.float32, [None, MAX_CAPTCHA*CHAR_SET_LEN])
keep_prob = tf.placeholder(tf.float32) # dropout

# 定义CNN
def crack_captcha_cnn(w_alpha=0.01, b_alpha=0.1):  # 这两个是定义初始时的值，比直接取0好一些
    x = tf.reshape(X, shape=[-1, IMAGE_HEIGHT, IMAGE_WIDTH, 1])
    #w_c1_alpha = np.sqrt(2.0/(IMAGE_HEIGHT*IMAGE_WIDTH)) #
    #w_c2_alpha = np.sqrt(2.0/(3*3*32))
    #w_c3_alpha = np.sqrt(2.0/(3*3*64))
    #w_d1_alpha = np.sqrt(2.0/(8*32*64))
    #out_alpha = np.sqrt(2.0/1024)

    # 3 conv layer
    w_c1 = tf.Variable(w_alpha*tf.random.normal([3, 3, 1, 32]))  # 产生一个随机的矩阵
    b_c1 = tf.Variable(b_alpha*tf.random.normal([32]))
    # tf.nn.conv2d函数是tensoflow里面的二维的卷积函数 x是图片的所有参数，W是此卷积层的权重 定义步长strides=[1,1,1,1]
    # strides[0]和strides[3]的两个1是默认值，中间两个1代表padding时在x方向运动一步，y方向运动一步，padding采用的方式是SAME。
    conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x, w_c1, strides=[1, 1, 1, 1], padding='SAME'), b_c1))
    conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv1 = tf.nn.dropout(conv1, keep_prob)

    w_c2 = tf.Variable(w_alpha*tf.random.normal([3, 3, 32, 64]))
    b_c2 = tf.Variable(b_alpha*tf.random.normal([64]))
    conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv1, w_c2, strides=[1, 1, 1, 1], padding='SAME'), b_c2))
    conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv2 = tf.nn.dropout(conv2, keep_prob)

    w_c3 = tf.Variable(w_alpha*tf.random_normal([3, 3, 64, 64]))
    b_c3 = tf.Variable(b_alpha*tf.random_normal([64]))
    conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv2, w_c3, strides=[1, 1, 1, 1], padding='SAME'), b_c3))
    conv3 = tf.nn.max_pool(conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv3 = tf.nn.dropout(conv3, keep_prob)

    # Fully connected layer
    w_d = tf.Variable(w_alpha*tf.random_normal([8*20*64, 1024]))
    b_d = tf.Variable(b_alpha*tf.random_normal([1024]))
    dense = tf.reshape(conv3, [-1, w_d.get_shape().as_list()[0]])
    dense = tf.nn.relu(tf.add(tf.matmul(dense, w_d), b_d))
    dense = tf.nn.dropout(dense, keep_prob)

    # w_out = tf.Variable(w_alpha*tf.random_normal([1024, MAX_CAPTCHA*CHAR_SET_LEN]))
    # b_out = tf.Variable(b_alpha*tf.random_normal([MAX_CAPTCHA*CHAR_SET_LEN]))
    # out = tf.add(tf.matmul(dense, w_out), b_out)
    #out = tf.nn.softmax(out)
    return dense
    # w_fc2 = tf.Variable(tf.truncated_normal([1024, 10], stddev=0.1))  # 输入是1024，最后的输出是10个
    # b_fc2 = tf.Variable(tf.constant(0.1, [32]))
    # prediction = tf.nn.softmax(tf.matmul(out, w_fc2) + b_fc2)
    # loss = tf.reduce_mean(-tf.reduce_sum(Y * tf.math.log(prediction), reduction_indices=[1]))
    # return loss

# 训练
def train_crack_captcha_cnn():
    output = crack_captcha_cnn()  # 定义CNN
    # loss = crack_captcha_cnn()  # 定义CNN
    predict = tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN])
    # print('!!!!!!!!!!!|')
    # loss
    # loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(output, Y))
    # print(output, Y)
    # Tensor("Add_1:0", shape=(?, 378), dtype=float32) Tensor("Placeholder_1:0", shape=(?, 378), dtype=float32)
    # Tensor("Add_1:0", shape=(?, 378), dtype=float32) Tensor("Placeholder_1:0", shape=(?, 378), dtype=float32)

    w_fc2 = tf.Variable(tf.truncated_normal([1024, 378], stddev=0.1))  # 输入是1024，最后的输出是10个
    b_fc2 = tf.Variable(tf.constant(0.1, shape=[378]))
    print(output.shape)  # (?, 1024)
    prediction = tf.nn.softmax(tf.matmul(output, w_fc2) + b_fc2)
    loss = tf.reduce_mean(-tf.reduce_sum(Y * tf.math.log(prediction), reduction_indices=[1]))
    print('!!!!!')
    # loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=output, labels=Y))  # todo，这里挂了
    # 最后一层用来分类的softmax和sigmoid有什么不同？
    # optimizer 为了加快训练 learning_rate应该开始大，然后慢慢衰
    optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)  # 机器学习的内容


    max_idx_p = tf.argmax(predict, 2)
    max_idx_l = tf.argmax(tf.reshape(Y, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
    correct_pred = tf.equal(max_idx_p, max_idx_l)
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        step = 0
        while True:
            batch_x, batch_y = get_next_batch(64)  # 这里的64是一维
            print(batch_x.shape, batch_y.shape)  # (64, 12000) (64, 378)
            #  run 每一次 training 的数据，逐步提升神经网络的预测准确性
            # 需要使用feed_dict这个字典来指定输入。
            _, loss_ = sess.run([optimizer, loss], feed_dict={X: batch_x, Y: batch_y, keep_prob: 0.75})
            print(step, loss_)

            # 每100 step计算一次准确率
            if step % 100 == 0:
                batch_x_test, batch_y_test = get_next_batch(100)
                acc = sess.run(accuracy, feed_dict={X: batch_x_test, Y: batch_y_test, keep_prob: 1.})
                print(step, acc)
                # 如果准确率大于50%,保存模型,完成训练
                if acc > 0.9:
                    saver.save(sess, "crack_capcha.model", global_step=step)
                    break
            step += 1

train_crack_captcha_cnn()