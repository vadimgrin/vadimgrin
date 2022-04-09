# Definition for singly-linked list.

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __str__(self):
        return str(self.val)


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        pass


def addNode(head, node):
    idx = head if head else node
    while idx.next:
        idx = idx.next
    idx.next = node
    return head


def printList(h):
    res = []
    while h.next:
        res.append(h.val)
        h = h.next
    res.append(h.val)
    return res


if __name__ == '__main__':
    l = [1, 3, 7, 4, 3, 1, 2]

    head = ListNode(l[0])
    for i in l[1:]:
        head = addNode(head, ListNode(i))

    print(f'My List: {printList(head)}')