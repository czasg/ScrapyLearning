import os

import cv2
import numpy as np
from PIL import Image
import pytesseract


def top(img,topnode, list2,list3):
    if len(topnode) == 1:
        if len(topnode[0]) >= 4:
            # 可以对比
            x = topnode[0][0][0]


            if 4 <= len(list2) <= 5:
                newx = list2[0][0]
                if 0 <= abs(newx - x) <= 2:
                    for ok in list2:
                        list3.append([ok[0], ok[1]])
    elif len(topnode)>1:
        for node in topnode:
            if 4 <= len(node) <= 5 and 4 <= len(list2) <= 5:
                be=node[0][0]
                fe=list2[0][0]
                if 0 <= abs(be - fe) <= 2:
                    for ok in list2:
                        list3.append([ok[0], ok[1]])
def scanning(ok, img, x, y):
    row, col = img.shape
    x2y = x_2y = xy2 = xy_2 = x2y2 = x_2y2 = x2y_2 = x_2y_2 = 1
    x2 = x + 2
    x_2 = x - 2
    y2 = y + 2
    y_2 = y - 2
    if 0 <= x2 < row:
        x2y = img[x2, y]  # （x+2,y）
        if 0 <= y2 < col:
            x2y2 = img[x2, y2]  # （x+2,y+2)
        if 0 <= y_2 < col:
            x2y_2 = img[x2, y_2]  # （x+2,y-2)
    if 0 <= x_2 < row:
        x_2y = img[x_2, y]  # (x-2,y)
        if 0 <= y2 < col:
            x_2y2 = img[x_2, y2]  # x-2，y+2
        if 0 <= y_2 < col:
            x_2y_2 = img[x_2, y_2]  # （x-2，y-2）
    if 0 <= y2 < col:
        xy2 = img[x, y2]  # （x,y+2）
    if 0 <= y_2 < col:
        xy_2 = img[x, y_2]  # (x,y-2)
    nodes = [x2y, x_2y, xy2, xy_2, x2y2, x_2y2, x2y_2, x_2y_2]

    if len([i for i in nodes if i == 0]) > 6:
        ok.append([x, y])


def nextpix(allnode, img, x, y, nodepass=True):
    num = img[x, y]
    h, w = img.shape[:2]
    if x < h - 1:
        if num == 0:

            if nodepass:
                nice = [[x, y]]
                allnode.append(nice)
                nodepass = False
                nextpix(allnode, img, x + 1, y, nodepass)
            else:
                node = allnode.pop()
                node.append([x, y])
                allnode.append(node)
                nextpix(allnode, img, x + 1, y, nodepass)
        else:
            nodepass = True
            nextpix(allnode, img, x + 1, y, nodepass)

nnn='1'
nn=[]
img = np.array(Image.open(nnn+'.jpg').convert('L'))
imgs = img.copy()
h, w = img.shape[:2]

for y in range(1, w):
    ok = []
    for x in range(1, h):
        num = img[x, y]
        if num > 127:
            img[x, y] = 255

        else:
            img[x, y] = 0
for y in range(1, w):
    node = []
    nextpix(node, img, 1, y)
    if len(node) == 1:
        for list in node:
            if len(list) == 5 or len(list) == 4:
                for xy in list:
                    nn.append([xy[0], xy[1]])
    elif len(node) > 1:

        for ll in node:
            if 4<=len(ll)<=5:

                befornode = []
                nextpix(befornode, img, 1, y - 1)

                top(img, befornode, ll,nn)

ooo=[]
for n in nn:
    img[n[0],n[1]]=255


result = cv2.blur(img, (2,2))
#
kernel2 = np.uint8(np.zeros((2, 2)))
opening = cv2.morphologyEx(img, cv2.MORPH_ELLIPSE, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1)))  # 闭运算
ojbk=cv2.erode(opening,kernel2)

# im_at_mean = cv2.adaptiveThreshold(ojbk, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 7)  # 自适应二值



# text = pytesseract.image_to_string(opening, config='-psm 7')
# print(text)
# cv2.imshow("soure",imgs)
cv2.imshow("ok",ojbk)

cv2.waitKey(0)

