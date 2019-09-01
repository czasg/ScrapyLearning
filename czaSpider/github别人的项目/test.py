import tensorflow as tf

# define placeholder for inputs to network
# xs = tf.placeholder(tf.float32, [None, 1])
# ys = tf.placeholder(tf.float32, [None, 1])
xs= tf.placeholder(tf.float32, [None, 1],name='x_in')
ys= tf.placeholder(tf.float32, [None, 1],name='y_in')

with tf.name_scope('inputs'):
    # define placeholder for inputs to network
    xs = tf.placeholder(tf.float32, [None, 1])
    ys = tf.placeholder(tf.float32, [None, 1])