from typing import List


def mysort(a: List[int]):
    again = True
    res = []
    count = 1
    while again:
        print(f'Pass {count}')
        again = False
        for i in range(1, len(a)):
            if a[i-1] > a[i]:
                a[i-1], a[i] = a[i], a[i-1]
                again = True
        count += 1
    return a


if __name__ == '__main__':
    a = [15, 12, 11, 11, 9,  7, 5, 3, 1]
    print(mysort(a))