"""
快速排序算法，左右两边端点，并以左端点为base
先从右往左，找出比base小的数，替换到left
然后从left开始从左往右，找出比base大的数，替换到right
此时left与right将会相等，此时此处置为base

此时base的左边一定比base小，右边一定比base大，base的位置基本可以定了
然后往两边散开递归

"""


def QuickSort(input_list, left, right):
    def division(input_list, left, right):
        base = input_list[left]
        while left < right:
            while left < right and base < input_list[right]:  # 在右边找到一个比之小的数
                right -= 1
            input_list[left] = input_list[right]
            while left < right and base > input_list[left]:  # 在左边找到一个比之大的数
                left += 1
            input_list[right] = input_list[left]
            print(input_list, '########')
        input_list[left] = base
        print(input_list)
        return left

    if left < right:
        base_index = division(input_list, left, right)
        QuickSort(input_list, left, base_index - 1)  # 往左往右分别进行，这是一个可怕的递归，得亏是共同维护一个list
        print('左边好了')
        QuickSort(input_list, base_index + 1, right)
        print('右边好了')


if __name__ == '__main__':
    # input_list = [6, 4, 8, 9, 2, 3, 1]
    input_list = [6, 4, 8, 9, 2, 3, 1, 123, 35, 1515, 0, 45]
    print('排序前:', input_list)
    QuickSort(input_list, 0, len(input_list) - 1)
    print('排序后:', input_list)
