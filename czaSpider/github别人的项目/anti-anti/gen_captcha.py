# coding:utf-8
from captcha.image import ImageCaptcha  # pip install captcha
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random, time, os

# 验证码中的字符, 就不用汉字了
number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']


# 验证码一般都无视大小写；验证码长度4个字符
def random_captcha_text(char_set=number + alphabet + ALPHABET, captcha_size=6):
    captcha_text = []
    for i in range(captcha_size):
        c = random.choice(char_set)
        captcha_text.append(c)
    return captcha_text


# 生成字符对应的验证码
def gen_captcha_text_and_image():
    # image = ImageCaptcha(160, 60)
    image = ImageCaptcha(200, 60)

    captcha_text = random_captcha_text()  # 获取四个随机
    captcha_text = ''.join(captcha_text)

    captcha = image.generate(captcha_text)
    # image.write(captcha_text, captcha_text + '.jpg')  # 写到文件

    # rm  =  'rm '+captcha_text + '.jpg'
    # print rm
    # os.system(rm)
    # time.sleep(10)

    captcha_image = Image.open(captcha)
    captcha_image = np.array(captcha_image)  # 所以训练图片实际就是提供正确的文字还有就是图片的矩阵。还可以。
    # print(captcha_image.shape)
    return captcha_text, captcha_image


def convert2gray(img):
    if len(img.shape) > 2:
        print(img.shape)
        # (60, 160, 3) 我去，生成的原来是三维的啊，这可让我有点吃惊
        gray = np.mean(img, -1)
        # 上面的转法较快，正规转法如下
        # r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
        # gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray
    else:
        return img


def char2pos(c):
    if c == '_':
        k = 62
        return k
    k = ord(c) - 48
    if k > 9:
        k = ord(c) - 55
        if k > 35:
            k = ord(c) - 61
            if k > 61:
                raise ValueError('No Map')
    return k

if __name__ == '__main__':
    # 测试
    # while (1):
    #     text, image = gen_captcha_text_and_image()
    #     print('begin ', time.ctime(), type(image))
    #     f = plt.figure()
    #     ax = f.add_subplot(111)
    #     ax.text(0.1, 0.9, text, ha='center', va='center', transform=ax.transAxes)
    #     plt.imshow(image)
    #
    #     plt.show()
    #     print('end ', time.ctime())

    #  (60, 160) 转化之后的shape
    # print(convert2gray(gen_captcha_text_and_image()[1]))
    # test = np.array([[[1, 2], [1, 'a'], [1, 2]],
    #                  [[1, 2], [1, 'b'], [1, 2]],
    #                  [[1, 2], [1, 2], [1, 8]],
    #                  [[1, 2], [1, 2], [1, 8]]])
    # print(test.shape)
    # print(np.mean(test))
    # print(np.mean(test, 0), np.mean(test, 0).shape)
    # print(np.mean(test, 1), np.mean(test, 1).shape)
    # print(np.mean(test, -1))
    # print(test.flatten())

    # print(len(ALPHABET))
    # print(char2pos('0'))
    # print(char2pos('1'))
    # print(char2pos('a'))
    # print(char2pos('A'))

    # print(np.zeros([2, 2 * 3]))

    test = np.zeros([5, 3])
    print(test[1,:])
    test[1,:] = np.ones(1).flatten() / 0.5
    print(test)
