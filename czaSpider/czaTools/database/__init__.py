# from czaSpider.czaTools import *
import numpy as np
import os
"""
命名规则：
get_data_for_xxx()
其中xxx是需要从此数据库中获取数据的函数方法名
"""
def get_data_for_img2num():
    trainingSet = [np.loadtxt(os.path.dirname(__file__) + os.sep +'img2num_value.txt'),]
    # trainingSet = [np.loadtxt((os.sep).join((os.path.dirname(__file__), 'img2num_value.txt')))]
    with open((os.path.dirname(__file__) + os.sep +'img2num_key.txt'),'r') as f_r:
    # with open((os.sep).join((os.path.dirname(__file__), 'img2num_key.txt')), 'r') as f_r:
        data = f_r.readline()
        hwLabels = [int(i) for i in data]
        trainingSet.append(hwLabels)
    return trainingSet