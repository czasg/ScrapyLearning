import os
import cv2
import numpy as np
import operator

from PIL import Image
from io import BytesIO

names = '4983571602'
current_path = os.path.dirname(os.path.abspath(__file__))


def file_load(file_path): return Image.open(file_path)


def img2gsi(picture, threshold=140):
    picture = picture.convert('L')
    coordinates = picture.load()
    width, height = picture.size
    for x in range(width):
        for y in range(height):
            coordinates[x, y] = 0 if coordinates[x, y] < threshold else 1
    return picture


def file_cutting(picture, cut_size, array=False):
    width, height = picture.size
    c_row, c_col = cut_size

    c_width = width // c_col  # 30
    c_height = height // c_row  # 28

    if array:
        result = [np.array(picture.crop((c * c_width, r * c_height, (c + 1) * c_width, (r + 1) * c_height)), 'f')
                  for r in range(c_row)
                  for c in range(c_col)]
        # result = np.array(result)
    else:
        result = [picture.crop((c * c_width, r * c_height, (c + 1) * c_width, (r + 1) * c_height))
                  for r in range(c_row)
                  for c in range(c_col)]
    return result


def box2vector(box):
    row, col = box.shape
    vector = np.zeros((1, row * col))
    count = 0
    for row in box:
        for gsi in row:
            vector[0, count] = gsi
            count += 1
    return vector


def file_save(pic_cut):
    for index, name in enumerate(names):
        pic_cut[index].save(name + '.png', 'PNG')


def api_spilt_pic():
    pic = os.path.join(current_path, '4983571602.png')
    pic = file_load(pic)
    cut_list = file_cutting(pic, (1, 10))
    file_save(cut_list)





def training_mat():  # 三维数组
    pic = os.path.join(current_path, '6666.png')
    pic = file_load(pic)
    pic = img2gsi(pic)
    cut_list = file_cutting(pic, (1, 10), array=True)
    cut_list = [box2vector(mat) for mat in cut_list]
    # print(cut_list[0].shape)
    np.save(names, cut_list)

    # pic = os.path.join(current_path, '4983571602.png')
    # pic = file_load(pic)
    # pic = img2gsi(pic)
    #
    # cut_list = file_cutting(pic, (1, 10), array=False)
    #
    # lis = []
    # for img in cut_list:
    #     # temp_file = BytesIO()
    #     img.save('temp.png', format='PNG')
    #     img = cv2.imread('temp.png', cv2.IMREAD_GRAYSCALE)
    #     lis.append(box2vector(img))
    # np.save(names, lis)
    # img = cv2.imdecode('', cv2.IMREAD_GRAYSCALE)

    # cut_list = [box2vector(mat) for mat in cut_list]
    # print(cut_list[0].shape)
    # np.save(names, cut_list)


def get_train_mat():
    train_mats = np.load('4983571602.npy', 'r+')
    return train_mats, [int(i) for i in '4983571602']


class KNN(object):
    def __init__(self, matData, k=3):
        self.matData = matData
        self.trainingSet = get_train_mat()
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
        trainMat = np.squeeze(trainMat)
        trainSetSize = trainMat.shape[0]
        print(trainMat.shape)
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
            vector = self.box2vector(matData)  # 1, 840
            res = self.classify(vector)
            list.append(res)
        return list


if __name__ == '__main__':
    pic = os.path.join(current_path, '4983571602.png')
    # print(pic)
    pic = file_load(pic)
    pic = img2gsi(pic)
    cut_list = file_cutting(pic, (1, 10), array=True)
    print(cut_list[0].shape)
    print(KNN(cut_list).res)

    # training_mat()

    # train, label = get_train_mat()
    # print(train[0].shape)
