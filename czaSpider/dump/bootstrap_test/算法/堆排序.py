"""
堆的基本属性parent
两个子节点: (2*parent)+1、(2*parent)+2
父节点：(parent-1)/2

小根堆、大根堆
"""

def HeadSort(input_list):
    def HeadAdjust(input_list, parent, length):
        parent_value = input_list[parent]
        child = 2 * parent + 1
        while child < length:
            if child + 1 < length and input_list[child + 1] > input_list[child]:
                child += 1
            if parent_value >= input_list[child]:
                break
            input_list[parent] = input_list[child]
            parent = child
            child = 2 * child + 1
        input_list[parent] = parent_value

    sorted_list = input_list
    length = len(sorted_list)
    for i in range(0, length // 2)[::-1]:
        HeadAdjust(sorted_list, i, length)

    for j in range(1, length)[::-1]:
        last = sorted_list[j]
        sorted_list[j] = sorted_list[0]
        sorted_list[0] = last

        HeadAdjust(sorted_list, 0, j)
        print('第%d趟排序:' % (length - j), end='')
        print(sorted_list)

    return sorted_list


if __name__ == '__main__':
    # input_list = [6, 4, 8, 9, 2, 3, 1]
    input_list = [ 1, 3, 4, 5, 2, 6, 9, 7, 8, 0 ]
    print('排序前:', input_list)
    sorted_list = HeadSort(input_list)
    print('排序后:', sorted_list)
