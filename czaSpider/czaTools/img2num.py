from PIL import Image
from io import BytesIO
import numpy as np
import requests
import operator
import os

from czaSpider.czaTools.database import get_data_for_img2num
from czaSpider.czaTools.path_func import to_path


class IMG(object):
    def __init__(self, pic, threshold=140, splitcoor=None):
        self.img = Image.open(pic)
        self.imgList = []  # finally result
        self.img2gsi(threshold)
        self.splitImg(splitcoor)

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

    def splitImg(self, coor):
        _row, _col = coor
        list = []
        num = 0
        height = self.row // _row
        weight = self.col // _col
        for r in range(_row):
            for c in range(_col):
                box = (c * weight, r * height, (c + 1) * weight, (r + 1) * height)
                list.append(np.array(self.img.crop(box), 'f'))
                num += 1
        self.imgList = list


class KNN(object):
    def __init__(self, matData, k=3):
        self.matData = matData
        self.trainingSet = get_data_for_img2num()
        self.vector = None
        self.vector = []
        self.k = k
        self.res = self.process_matData()

    def box2vector(self, box):
        row, col = box.shape
        vector = np.zeros((1, row * col))
        count = 0
        for row in box:
            for gsi in row:
                vector[0, count] = gsi
                count += 1
        return vector

    def classify(self, matData):
        trainMat, trainLabel = self.trainingSet
        trainSetSize = trainMat.shape[0]
        diffMat = np.tile(matData, (trainSetSize, 1)) - trainMat
        squareDiff = diffMat ** 2
        squareDiffDistance = squareDiff.sum(axis=1)
        distances = squareDiffDistance ** 0.5
        sortedDistIndicies = distances.argsort()
        classCount = {}
        for i in range(self.k):
            kLabel = trainLabel[sortedDistIndicies[i]]
            classCount[kLabel] = classCount.get(kLabel, 0) + 1
        resSorted = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
        return resSorted[0][0]

    def process_matData(self):
        list = []
        for matData in self.matData:
            vector = self.box2vector(matData)
            res = self.classify(vector)
            list.append(res)
        return list


# main interface from path
def img2num(picture, threshold=140, coor=(1, 10)):
    picture = IMG(picture, threshold, splitcoor=coor)
    knn = KNN(picture.imgList)
    return knn.res


# main interface from url
def img2num_from_url(picture, threshold=140, coor=(1, 10)):
    picture = IMG(url2bytes(picture), threshold, splitcoor=coor)
    knn = KNN(picture.imgList)
    return knn.res


def url2bytes(url):
    return BytesIO(requests.get(url).content)


def get_name(file):
    return os.path.basename(file).split(".")[0]


def file_download(fileUrl):
    project_path = os.path.dirname(os.path.dirname(__file__))
    file_name = os.path.basename(fileUrl)
    file_path = to_path(project_path, "dump", file_name)
    with open(file_path, 'wb') as file:
        file.write(requests.get(fileUrl).content)
    return file_path


def file_remove(fileUrl):
    os.remove(fileUrl)
    if not os.path.exists(fileUrl):
        return True
    return file_remove(fileUrl)
