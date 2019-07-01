"""
对于N个数据，遍历(N-1)(N-1)次，每次对比相邻的两数，对两数进行排序

"""

def bubbleSort(input_list):
	if len(input_list) == 0:
		return []
	sorted_list = input_list
	for i in range(len(sorted_list) - 1):
		print('第%d趟排序:' % (i + 1))
		for j in range(len(sorted_list) - 1):
			if sorted_list[j + 1] < sorted_list[j]:
				sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
			print(sorted_list)
	return sorted_list

if __name__ == '__main__':
	input_list = [50, 123, 543, 187, 49, 30, 0, 2, 11, 100]
	print('排序前:', input_list)
	sorted_list = bubbleSort(input_list)
	print('排序后:', sorted_list)