"""
以第一个端点数未基准，首先遍历后面的(N-1)次，每次的数，与前面的值进行比对、排序

"""

def insertSort(input_list):
    sorted_list = input_list

    for i in range(1, len(sorted_list)):
        current = sorted_list[i]
        pre = i - 1
        while pre >= 0 and current < sorted_list[pre]:
            sorted_list[pre + 1] = sorted_list[pre]
            pre -= 1
        sorted_list[pre + 1] = current
        print(sorted_list)
    return sorted_list


if __name__ == '__main__':
    input_list = [6, 4, 8, 9, 2, 3, 1]
    print('排序前:', input_list)
    sorted_list = insertSort(input_list)
    print('排序后:', sorted_list)