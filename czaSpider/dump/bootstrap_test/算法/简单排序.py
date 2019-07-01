"""
首先需要遍历(N)次，从第一个端点值开始，假设此值为最小，然后遍历(N-i)次，是否存在比之更小的值
存在则交换

"""

def SelectSort(input_list):
    sorted_list = input_list
    length = len(input_list)
    for i in range(length):
        min_index = i
        for j in range(i + 1, length):
            if sorted_list[min_index] > sorted_list[j]:
                min_index = j
        if min_index == i:
            continue
        min_value = sorted_list[min_index]
        sorted_list[min_index] = sorted_list[i]
        sorted_list[i] = min_value
    return sorted_list


if __name__ == '__main__':
    input_list = [6, 4, 8, 9, 2, 3, 1]
    print('排序前:', input_list)
    sorted_list = SelectSort(input_list)
    print('排序后:', sorted_list)
