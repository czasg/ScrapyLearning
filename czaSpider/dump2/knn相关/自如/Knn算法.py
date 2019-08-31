import numpy as np

from PIL import Image
from collections import OrderedDict


class KNN:
    def __init__(self):
        self.k = 3
        self.train_matrix = np.loadtxt('img2num_value.txt')
        self.train_labels = '0123456789'

    def matrix2vector(self, matrix: np.ndarray):
        return np.array([[point_gsi for each_row in matrix for point_gsi in each_row]])

    def calculate(self, matrix: np.ndarray):
        trainSetSize = self.train_matrix.shape[0]
        diffMatrix = np.tile(matrix, (trainSetSize, 1)) - self.train_matrix
        return (diffMatrix ** 2).sum(axis=1) ** 0.5

    def classify(self, distances):
        assert len(distances.shape) == 1
        distancesSortedIndex = distances.argsort()
        knn_pool = OrderedDict()
        for index in range(self.k):
            kLabel = self.train_labels[distancesSortedIndex[index]]
            knn_pool[kLabel] = knn_pool.get(kLabel, 0) + 1
        return sorted(knn_pool.items(), key=lambda x: x[1], reverse=True)[0][0]


if __name__ == '__main__':
    pass
    # for i in range(10):
    #     img = np.array(Image.open('test_%d.png' % i))
    #     img = KNN.matrix2vector(img)
    #     distances = KNN.calculate(img)
    #     print(KNN.classify(distances))
