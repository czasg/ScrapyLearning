import cv2
import numpy as np

# for i in range(10):
#     img = cv2.imread('test_%d.png' % i, cv2.IMREAD_GRAYSCALE)
#     # print("cv2.imread(imgfile, cv2.IMREAD_GRAYSCALE)结果如下：")
#     # print('大小：{}'.format(img.shape))
#     # print("类型：%s"%type(img))
#     # print(img)
#     # print(type(img))
#     np.savetxt('temp_%d.txt'%i,img)

# with open('temp_0.txt', 'r') as f:
# #     for i,j in enumerate(f.readlines()):
# #         print(len(j))
#     # print(len(f.readline()))  # 一共28行，每行750个数据
#     a = ' '.join([i.strip() for i in f.readlines()])
# with open('aim.txt', 'a+') as f:
#     f.write(a + '\n')

# a = np.loadtxt('temp_0.txt')
# print(a.shape)

for i in range(10):
    with open('temp_%d.txt' % i, 'r') as f:
        a = ' '.join([i.strip() for i in f.readlines()])
    with open('aim.txt', 'a+') as f:
        f.write(a + '\n')