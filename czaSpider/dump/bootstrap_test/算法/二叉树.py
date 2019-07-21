import sys


class Node(object):
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def pre(root):
    if root == None:
        return
    print(root.value)
    pre(root.left)
    pre(root.right)


def mid(root):
    if root == None:
        return
    mid(root.left)
    print(root.value)
    mid(root.right)


def aft(root):
    if root == None:
        return
    aft(root.left)
    aft(root.right)
    print(root.value)


root = Node('D', Node('B', Node('A'), Node('C')), Node('E', right=Node('G', Node('F'))))
print('前序遍历：')
pre(root)
print('\n')
print('中序遍历：')
mid(root)
print('\n')
print('后序遍历：')
aft(root)
