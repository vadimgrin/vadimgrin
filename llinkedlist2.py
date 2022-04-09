from typing import List, Any


class Node:
    def __init__(self, val, next = None):
        self.val = val
        self.next = next


def printList(head):
    res = []
    while head.next:
        res.append(head.val)
        head = head.next
    res.append(head.val)
    return res


def addNode(h: Node, n: Node):
    if not h:
        return n
    while h.next:
        h = h.next
    h.val = n
    return h


def list2number(h: Node):
    ret = 0
    mult = 1
    while h.next:
        ret += mult * h.val
        mult *= 10
        h = h.next
    return ret


def num2list(num: int):
    ret = []
    m = 10
    while num > 0:
        r = num % m
        ret.append(r)
        num = num - r
        m *= 10
    return ret


class Solution:
    def removeNthFromEnd(self, head: List[int], n: int):
        fast = slow = head
        for _ in range(n):
            fast = fast.next
        if not fast:
            return head.next
        while fast.next:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next
        return head


if __name__ == '__main__':
    # s = Solution()
    # head = None
    # for i in [3, 4, 11, 17, 8, 3, 7]:
    #     head = addNode(head, Node(i))
    #
    # print(printList(head))
    # s.removeNthFromEnd(head, 3)
    # print(printList(head))

    for n in [12, 0, 3, 3354, 23, 45]:
        print(f'{n}: {num2list(n)}')
