from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pytesseract

ok = []


def scanning(img, x, y, row, col):
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


img = np.array(Image.open('3_3.jpg').convert('L'))

rows, cols = img.shape

for i in range(rows):
    for j in range(cols):
        if (img[i, j] <= 128):
            img[i, j] = 0
        else:
            img[i, j] = 1

for i in range(rows):
    for j in range(cols):
        scanning(img, i, j, rows, cols)
for i in ok:
    img[i[0], i[1]] = 0

text = pytesseract.image_to_string(img, config='-psm 7')
print(text)

plt.imshow(img, cmap='gray')

plt.show()
