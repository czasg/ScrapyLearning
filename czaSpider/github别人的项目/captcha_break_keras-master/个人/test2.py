import os
os.environ['KERAS_BACKEND']='theano'

import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.models import Sequential
from keras.layers import Dense


