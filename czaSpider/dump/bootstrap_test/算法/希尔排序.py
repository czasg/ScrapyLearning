"""
希尔排序与直接插入排序相比较，其实二者是有很大程度上的相似的
希尔排序最后一定最完全执行一遍直接插入排序

直接插入排序是稳定的，而希尔排序是不稳定的
直接插入排序更适合于原始记录基本有序的集合
希尔排序则比较次数与移动次数比直接插入排序少很多

直接插入排序使用与链式存储结构
"""


def shellSort(input_list):
    length = len(input_list)
    sorted_list = input_list
    gap = length // 2
    while gap > 0:
        for i in range(gap, length):
            current = sorted_list[i]
            pre = i - gap
            while pre >= 0 and current < sorted_list[pre]:
                sorted_list[pre + 1] = sorted_list[pre]
                pre -= gap
            sorted_list[pre + gap] = current
        gap //= 2
    return sorted_list


if __name__ == '__main__':
    input_list = [50, 123, 543, 187, 49, 30, 0, 2, 11, 100]
    print('排序前:', input_list)
    sorted_list = shellSort(input_list)
    print('排序后:', sorted_list)
