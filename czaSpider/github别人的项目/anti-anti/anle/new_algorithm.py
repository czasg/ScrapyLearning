import numpy as np
import cv2
from PIL import Image

number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']


def resolve(img, imgs):
    pix = img.load()
    width = img.size[0]
    height = img.size[1]
    for x in range(width):

        for y in range(height):
            if 0 <= y < 2 or 0 <= x < 2:
                imgs[y, x, 0] = 255
                imgs[y, x, 1] = 255
                imgs[y, x, 2] = 255
            r, g, b = pix[x, y]  # pix获取rgb值
            if 100 <= r <= 130 and 100 <= g <= 130 and 100 <= b <= 130:
                imgs[y, x, 0] = 255
                imgs[y, x, 1] = 255
                imgs[y, x, 2] = 255


def todo(filename):
    imgs = cv2.imread(filename)
    img = Image.open(filename)
    resolve(img, imgs)

    im_gray = cv2.cvtColor(imgs, cv2.COLOR_BGR2GRAY)  # 灰度
    kernel2 = np.uint8(np.zeros((3, 3)))
    opening = cv2.morphologyEx(im_gray, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)))  # 闭运算
    ojbk = cv2.erode(opening, kernel2)
    im_at_mean = cv2.adaptiveThreshold(ojbk, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 7)  # 自适应二值
    return im_at_mean


def filter(text):
    text = text.replace("V", "Y").replace('v', "Y")
    return text


if __name__ == '__main__':
    print(todo("3.jpg"))

    img = todo('3.jpg')
    cv2.imwrite("3_3.jpg", img)
