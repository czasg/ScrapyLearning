from PIL import Image
from io import BytesIO
import numpy as np


class KNN:
    k = 3
    train_matrix = np.array([[1, 1, 1, 1, 1, 1], [2 for _ in range(6)], [3 for _ in range(6)],
                             [4 for _ in range(6)], [5 for _ in range(6)], [6 for _ in range(6)]])
    train_labels = ['1', '2', '3', '4', '5', '6']

    @classmethod
    def matrix2vector(cls, matrix: np.ndarray):
        return np.array([[point_gsi for each_row in matrix for point_gsi in each_row]])

    @classmethod
    def calculate(cls, matrix: np.ndarray):
        trainSetSize = cls.train_matrix.shape[0]
        diffMatrix = np.tile(matrix, (trainSetSize, 1)) - cls.train_matrix
        return (diffMatrix ** 2).sum(axis=1) ** 0.5

    @classmethod
    def classify(cls, distances):
        assert len(distances.shape) == 1
        distancesSortedIndex = distances.argsort()
        knn_pool = {}
        for index in range(cls.k):
            kLabel = cls.train_labels[distancesSortedIndex[index]]
            knn_pool[kLabel] = knn_pool.get(kLabel, 0) + 1
        return sorted(knn_pool.items(), key=lambda x: x[1], reverse=True)[0][0]


if __name__ == '__main__':
    a = np.array([[3, 3, 3], [4, 4, 4]])
    a = KNN.matrix2vector(a)
    b = np.array([[5, 5, 5], [5, 5, 5]])
    b = KNN.matrix2vector(b)
    c = np.array([[1, 1, 1], [1, 1, 1]])
    c = KNN.matrix2vector(c)
    d = np.array([[3, 3, 3], [3, 3, 3]])
    d = KNN.matrix2vector(d)
    aim = np.array([a, b, c, d])
    for i in aim:
        distances = KNN.calculate(i)
        print(KNN.classify(distances))
