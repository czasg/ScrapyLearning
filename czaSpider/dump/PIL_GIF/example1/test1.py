import numpy as np
from PIL import Image
from images2gif import writeGif
outfilename = "my.gif" # 转化的GIF图片名称
filenames = []         # 存储所需要读取的图片名称
# current
for i in range(1, 11):   # 读取100张图片
    filename = str(i) + '.jpg'    # path是图片所在文件，最后filename的名字必须是存在的图片
    filenames.append(filename)              # 将使用的读取图片汇总
frames = []
for image_name in filenames:                # 索引各自目录
    im = Image.open(image_name)             # 将图片打开，本文图片读取的结果是RGBA格式，如果直接读取的RGB则不需要下面那一步
    im = im.convert("RGB")                  # 通过convert将RGBA格式转化为RGB格式，以便后续处理
    im = np.array(im)                       # im还不是数组格式，通过此方法将im转化为数组
    frames.append(im)                       # 批量化
writeGif(outfilename, frames, duration=0.1, subRectangles=False)