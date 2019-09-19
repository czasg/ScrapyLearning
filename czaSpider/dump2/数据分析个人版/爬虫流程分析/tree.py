import math,numpy,operator

def createDataSet(): # the first and second cols in dataSet is matching the labels
	dataSet = [[1,1,1,'yes'], # this row mean both of labels[0]  and labels[1] are 1
	           [1,1,0,'NA'],
	           [1,0,0,'no'],
	           [0,0,1,'no'],
	           [0,1,0,'yes']]
	labels = ['no surfacing','flippers','temp']
	return dataSet,labels

def calcShannonEnt(dataSet):
	numEntries = len(dataSet) # the statistics of num from dataSet
	labelCounts = {}
	for eachVac in dataSet: # traversing the source data of dataSet
		currentLabel = eachVac[-1] # fetch the last cloimns in the result of traversal
		if currentLabel not in labelCounts.keys():
			labelCounts[currentLabel] = 0 # distinguishing by the last column? it has only yes or no
		labelCounts[currentLabel] += 1 # statistics for the count of each yes or no?
	tempShannonEnt = 0.0 # initing the retropy
	for key in labelCounts:
		prob = float(labelCounts[key])/numEntries
		tempShannonEnt -= prob * math.log(prob,2)
	return tempShannonEnt # the retropy is true calculing by p*log(p,2), but it is not by the cloumn except the last one, which cover just yes or no

def splitDataSet(dataSet,axis,value):
	tempDataSet = []
	for eachVec in dataSet:
		if eachVec[axis] == value:
			reduceDataVec = eachVec[:axis]
			reduceDataVec.extend(eachVec[axis+1:])
			tempDataSet.append(reduceDataVec)
	return tempDataSet

def chooseBestFeatureToSplit(dataSet):
	numFeatures = len(dataSet[0]) - 1 # if you have three cols, you just need to care except of last cols, which is criteria including yes or no
	baseEntropy = calcShannonEnt(dataSet) # marking the prime retrop
	bestInfoGain = 0.0; bestFeature = -1
	for i in range(numFeatures):
		tempList = [example[i] for example in dataSet]
		uniqueVals = set(tempList)
		newEntropy = 0.0
		for eachVal in uniqueVals:
			tempSplitResult = splitDataSet(dataSet,i,eachVal)
			prob = len(tempSplitResult)/float(len(dataSet))
			#print(len(tempSplitResult),float(len(dataSet)))
			#print('prob in chooseBestFeatureToSplit is: %s'%prob)
			newEntropy += prob * calcShannonEnt(tempSplitResult)
		infoGain = baseEntropy - newEntropy
		print(infoGain)
		if infoGain >= bestInfoGain:
			bestInfoGain = infoGain
			bestFeature = i
	return bestFeature

def majorityCnt(classList):
	classCount = {}
	for eachVal in classList:
		if eachVal not in classCount.keys():
			classCount[eachVal] = 0
		classCount[eachVal] += 1
	sortedClassCount = sorted(classCount.items(),
		key = operator.itemgetter(1), reverse = True)
	return sortedClassCount[0][0]

def createTree(dataSet,labels):
	classList = [example[-1] for example in dataSet]
	if classList.count(classList[0]) == len(classList):
		return classList[0]
	if len(dataSet[0]) == 1:
		return majorityCnt(classList)
	indexBestFeature = chooseBestFeatureToSplit(dataSet)
	labelBestFeature = labels[indexBestFeature]
	myTree = {labelBestFeature:{}}
	del(labels[indexBestFeature])
	tempValues = [example[indexBestFeature] for example in dataSet]
	uniqueVals = set(tempValues)
	for value in uniqueVals:
		splitDataSet1 = splitDataSet(dataSet,indexBestFeature,value)
		subLabels = labels[:]
		myTree[labelBestFeature][value] = createTree(splitDataSet1,
			subLabels)
	return myTree

def test():
	dataSet,labels = createDataSet()
	myTree = createTree(dataSet,labels)
	print(myTree)

if __name__ == '__main__':
	test()
	# from collections import deque
	# labels = deque()
	# labels.append('1')
