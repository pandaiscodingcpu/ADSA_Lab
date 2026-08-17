class Node:
    def __init__(self,key):
        self.key = key
        self.right = None
        self.left = None

def new(key):
    return Node(key)


def rotate_right(x):
    y = x.left
    x.left = y.right
    y.right = x
    return y

def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    return y

def splay(root, key):
    if root is None :
      return  new(key)
    if root.key == key:
        return root

    if root.key > key:
        if root.left is None:
            return root
        if root.left.key > key:
            root.left.left = splay(root.left.left, key)
            root = rotate_right(root)
        elif root.left.key < key:
            root.left.right = splay(root.left.right, key)
            if root.left.right:
                root.left = rotate_left(root.left)
        return root.left if root.left is None else rotate_right(root)
    else:
        if root.right is None:
            return root
        if root.right.key > key:
            root.right.left = splay(root.right.left, key)
            if root.right.left:
                root.right = rotate_right(root.right)
        elif root.right.key < key:
            root.right.right = splay(root.right.right, key)
            root = rotate_left(root)
        return root.right if root.right is None else rotate_left(root)

def insert(root, key):
    if root is None:
        return new(key)

    root = splay(root, key)

    if root.key == key:
        return root

    node = new(key)
    if root.key > key:
        node.right = root
        node.left = root.left
        root.left = None
    else:
        node.left = root
        node.right = root.right
        root.right = None
    return node

def pre_order(node):
    if node:
        print(node.key, end=" ")
        pre_order(node.left)
        pre_order(node.right)

if __name__ == "__main__":
    root = None
    root = insert(root, 100)
    root = insert(root, 50)
    root = insert(root, 200)
    root = insert(root, 40)
    root = insert(root, 60)
    print("Preorder traversal of the modified Splay tree:")
    pre_order(root)
