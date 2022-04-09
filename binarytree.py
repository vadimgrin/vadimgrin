# A class to store a BST node
class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


# Function to perform inorder traversal on the BST
def inorder(root):
    if root is None:
        return

    inorder(root.left)
    print(root.data, end=' ')
    inorder(root.right)


# Recursive function to insert a key into a BST
def insert(root, key):
    # if the root is None, create a new node and return it
    if root is None:
        return Node(key)

    # if the given key is less than the root node, recur for the left subtree
    if key < root.data:
        root.left = insert(root.left, key)

    # if the given key is more than the root node, recur for the right subtree
    else:
        root.right = insert(root.right, key)

    return root


# Function to delete a smallest node from a BST
def deleteMinNode(root):
    while root.left:
        root = root.left

    return root


if __name__ == '__main__':

    keys = [15, 10, 20, 8, 12, 16]

    root = None
    for key in keys:
        root = insert(root, key)

    inorder(root)
    node = deleteMinNode(root)
    print(node.data)
    inorder(root)
