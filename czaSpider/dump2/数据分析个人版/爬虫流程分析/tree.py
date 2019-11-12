import math
import operator


class DecisionTree:

    @classmethod
    def calcShannonEnt(cls, dataSet):
        numEntries = len(dataSet)
        labelCounts = {}
        for eachVac in dataSet:
            currentLabel = eachVac[-1]
            if currentLabel not in labelCounts.keys():
                labelCounts[currentLabel] = 0
            labelCounts[currentLabel] += 1
        tempShannonEnt = 0.0
        for key in labelCounts:
            prob = float(labelCounts[key]) / numEntries
            tempShannonEnt -= prob * math.log(prob, 2)
        return tempShannonEnt

    @classmethod
    def splitDataSet(cls, dataSet, axis, value):
        tempDataSet = []
        for eachVec in dataSet:
            if eachVec[axis] == value:
                reduceDataVec = eachVec[:axis]
                reduceDataVec.extend(eachVec[axis + 1:])
                tempDataSet.append(reduceDataVec)
        return tempDataSet

    @classmethod
    def chooseBestFeatureToSplit(cls, dataSet):
        numFeatures = len(dataSet[0]) - 1
        baseEntropy = cls.calcShannonEnt(dataSet)
        bestInfoGain = 0.0
        bestFeature = -1
        for i in range(numFeatures):
            tempList = [example[i] for example in dataSet]
            uniqueVals = set(tempList)
            newEntropy = 0.0
            for eachVal in uniqueVals:
                tempSplitResult = cls.splitDataSet(dataSet, i, eachVal)
                prob = len(tempSplitResult) / float(len(dataSet))
                newEntropy += prob * cls.calcShannonEnt(tempSplitResult)
            infoGain = baseEntropy - newEntropy
            if infoGain >= bestInfoGain:
                bestInfoGain = infoGain
                bestFeature = i
        return bestFeature

    @classmethod
    def majorityCnt(cls, classList):
        classCount = {}
        for eachVal in classList:
            if eachVal not in classCount.keys():
                classCount[eachVal] = 0
            classCount[eachVal] += 1
        sortedClassCount = sorted(classCount.items(),
                                  key=operator.itemgetter(1), reverse=True)
        return sortedClassCount[0][0]


def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return DecisionTree.majorityCnt(classList)
    indexBestFeature = DecisionTree.chooseBestFeatureToSplit(dataSet)
    labelBestFeature = labels[indexBestFeature]
    myTree = {labelBestFeature: {}}
    del (labels[indexBestFeature])
    tempValues = [example[indexBestFeature] for example in dataSet]
    uniqueVals = set(tempValues)
    for value in uniqueVals:
        splitDataSet1 = DecisionTree.splitDataSet(dataSet, indexBestFeature, value)
        subLabels = labels[:]
        myTree[labelBestFeature][value] = createTree(splitDataSet1,
                                                     subLabels)
    return myTree


if __name__ == '__main__':
    test1 = [
        [1,1,1,'男'],
        [1,0,1,'男'],
        [0,1,1,'男'],
        [0,0,1,'男'],
        [0,1,1,'女'],
        [0,1,0,'女'],
        [0,0,0,'女'],
    ]
    test2 = ['高', '壮', '大']
    print(createTree(test1, test2))