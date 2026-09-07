class Node:
    def __init__(self, point, left=None, right=None):
        self.point = point  # List or tuple representing coordinates
        self.left = left    # Left child node
        self.right = right  # Right child node


class KDTree:
    def __init__(self, k):
        self.k = k  # Number of dimensions (e.g., 2 for 2D space)
        self.root = None

    def insert(self, point):
        """Insert a point into the KD-Tree."""
        if len(point) != self.k:
            raise ValueError(f"Point dimension must match tree dimension ({self.k})")
        self.root = self._insert_rec(self.root, point, depth=0)

    def _insert_rec(self, root, point, depth):
        if root is None:
            return Node(point)
        
        # Select axis based on depth modulo dimensions
        axis = depth % self.k
        
        if point[axis] < root.point[axis]:
            root.left = self._insert_rec(root.left, point, depth + 1)
        else:
            root.right = self._insert_rec(root.right, point, depth + 1)
        return root

    def search(self, point):
        """Search for an exact point in the KD-Tree."""
        return self._search_rec(self.root, point, depth=0)

    def _search_rec(self, root, point, depth):
        if root is None:
            return False
        if list(root.point) == list(point):
            return True
        
        axis = depth % self.k
        if point[axis] < root.point[axis]:
            return self._search_rec(root.left, point, depth + 1)
        else:
            return self._search_rec(root.right, point, depth + 1)

    def delete(self, point):
        """Delete a point from the KD-Tree."""
        self.root = self._delete_rec(self.root, point, depth=0)

    def _find_min(self, root, axis, depth):
        """Find the node with the minimum value along a specific axis."""
        if root is None:
            return None
        
        curr_axis = depth % self.k
        
        if curr_axis == axis:
            if root.left is None:
                return root
            return self._min_node(root, self._find_min(root.left, axis, depth + 1), root.right, axis)
        else:
            left_min = self._find_min(root.left, axis, depth + 1)
            right_min = self._find_min(root.right, axis, depth + 1)
            return self._min_node(root, left_min, right_min, axis)

    def _min_node(self, n1, n2, n3, axis):
        m = n1
        if n2 is not None and n2.point[axis] < m.point[axis]:
            m = n2
        if n3 is not None and n3.point[axis] < m.point[axis]:
            m = n3
        return m

    def _delete_rec(self, root, point, depth):
        if root is None:
            return None
        
        axis = depth % self.k
        
        # If point is found at current root
        if list(root.point) == list(point):
            # Case 1: If right child is not None, find minimum in right subtree
            if root.right is not None:
                min_node = self._find_min(root.right, axis, depth + 1)
                root.point = min_node.point
                root.right = self._delete_rec(root.right, min_node.point, depth + 1)
            # Case 2: If right is None but left is not, find minimum in left subtree, 
            # move it to right, and clear left subtree
            elif root.left is not None:
                min_node = self._find_min(root.left, axis, depth + 1)
                root.point = min_node.point
                root.right = self._delete_rec(root.left, min_node.point, depth + 1)
                root.left = None
            # Case 3: If both children are None, node is a leaf
            else:
                return None
            return root
        
        if point[axis] < root.point[axis]:
            root.left = self._delete_rec(root.left, point, depth + 1)
        else:
            root.right = self._delete_rec(root.right, point, depth + 1)
        return root

    def display(self):
        """Display the tree structure visually."""
        print("KD-Tree Structure:")
        self._display_rec(self.root, depth=0, prefix="Root: ")

    def _display_rec(self, root, depth, prefix):
        if root is not None:
            print("  " * (depth * 2) + prefix + str(root.point))
            if root.left is not None or root.right is not None:
                if root.left:
                    self._display_rec(root.left, depth + 1, "L--- ")
                else:
                    print("  " * ((depth + 1) * 2) + "L--- None")
                if root.right:
                    self._display_rec(root.right, depth + 1, "R--- ")
                else:
                    print("  " * ((depth + 1) * 2) + "R--- None")

if __name__ == "__main__":
    # Create a 2-Dimensional KD-Tree
    kdtree = KDTree(k=2)

    # 1. Insertions
    points = [(3, 6), (17, 15), (13, 15), (6, 12), (9, 1), (2, 7)]
    for p in points:
        kdtree.insert(p)
    
    print("--- Initial Tree ---")
    kdtree.display()

    # 2. Searching
    query = (6, 12)
    print(f"\nSearching for point {query}: {'Found' if kdtree.search(query) else 'Not Found'}")
    
    query_missing = (99, 99)
    print(f"Searching for point {query_missing}: {'Found' if kdtree.search(query_missing) else 'Not Found'}")

    # 3. Deletion
    print(f"\nDeleting point (3, 6)...")
    kdtree.delete((3, 6))

    # 4. Display Tree after deletion
    print("\n--- Tree After Deletion ---")
    kdtree.display()