import re
import cv2
from PIL import Image
import numpy as np


class IMG(object):
    def __init__(self, pic, threshold=140):
        self.img_name = (re.search('.*/(.*)', pic).group(1) if '/' in pic else pic).split('.')[0]
        self.img = Image.open(pic)
        self.img = self.img.resize((300, 30), Image.ANTIALIAS)
        self.img2gsi(threshold)

    def img2gsi(self, threshold):
        self.img = self.img.convert('L')
        coorData = self.img.load()
        self.col, self.row = self.img.size
        for x in range(self.col):
            for y in range(self.row):
                if coorData[x, y] > threshold:
                    coorData[x, y] = 1
                else:
                    coorData[x, y] = 0

    def split_img_and_save(self, coor):
        _row, _col = coor
        height = self.row // _row
        weight = self.col // _col
        num = 0
        for r in range(_row):
            for c in range(_col):
                box = (c * weight, r * height, (c + 1) * weight, (r + 1) * height)
                self.img.crop(box).save('test_%s.png' % self.img_name[num])
                num += 1


def get_txt():
    for i in range(10):
        img = cv2.imread('test_%d.png' % i, cv2.IMREAD_GRAYSCALE)
        np.savetxt('temp_%d.txt' % i, img)
    for i in range(10):
        with open('temp_%d.txt' % i, 'r') as f:
            a = ' '.join([i.strip() for i in f.readlines()])
        with open('aim.txt', 'a+') as f:
            f.write(a + '\n')


if __name__ == '__main__':
    a = IMG('6948527301.png')
    a.split_img_and_save((1, 10))
    get_txt()
