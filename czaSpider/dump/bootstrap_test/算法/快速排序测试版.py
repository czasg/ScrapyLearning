def test(alists, left, right):
    def to(alists, left, right):
        base = alists[left]
        while left < right:

            while left < right and base < alists[right]:
                right -= 1
            alists[left], alists[right] = alists[right], alists[left]

            while left < right and alists[left] < base:
                left += 1
            alists[left], alists[right] = alists[right], alists[left]

        return left

    if left < right:
        index = to(alists, left, right)
        test(alists, left, index - 1)
        test(alists, index + 1, right)


if __name__ == '__main__':
    input_list = [6, 4, 8, 9, 2, 3, 1, 123, 35, 1515, 0, 45]
    test(input_list, 0, len(input_list) - 1)
    print(input_list)
