from PIL import Image
import numpy as np


class IMG(object):
    def __init__(self, pic, threshold=140, splitcoor=None):
        self.img = Image.open(pic)
        # self.img = self.img.resize((300, 30), Image.ANTIALIAS)
        self.imgList = []  # finally result
        self.img2gsi(threshold)
        # self.splitImg(splitcoor)

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
                self.img.crop(box).save('test_%d.jpg' % num)
                num += 1


if __name__ == '__main__':
    a = IMG('9635804271.png')
    a.split_img_and_save((1, 10))