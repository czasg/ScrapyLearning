import cv2
import numpy as np

# for i in range(10):
#     img = cv2.imread('test_%d.jpg' % i, cv2.IMREAD_GRAYSCALE)
#     print("cv2.imread(imgfile, cv2.IMREAD_GRAYSCALE)结果如下：")
#     print('大小：{}'.format(img.shape))
#     print("类型：%s"%type(img))
#     print(img)
#     print(type(img))
#     np.savetxt('temp_%d.txt'%i,img)

with open('temp_0.txt', 'r') as f:
    for i,j in enumerate(f.readlines()):
        print(i)

# a = np.loadtxt('temp_0.txt')
# print(a.shape)