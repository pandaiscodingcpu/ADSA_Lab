from bisect import bisect_left, bisect_right


class BPlusTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []

        # For internal nodes
        self.children = []

        # For leaf nodes
        self.next = None


class BPlusTree:
    def __init__(self, order=4):
        self.order = order
        self.root = BPlusTreeNode(leaf=True)

    # ---------------------------------------------------------
    # SEARCH OPERATION
    # ---------------------------------------------------------
    def search(self, key):
        current = self.root

        # Traverse from root to leaf
        while not current.leaf:
            index = bisect_right(current.keys, key)
            current = current.children[index]

        # Search in leaf node
        index = bisect_left(current.keys, key)

        if index < len(current.keys) and current.keys[index] == key:
            return True

        return False

    # ---------------------------------------------------------
    # INSERTION OPERATION
    # ---------------------------------------------------------
    def insert(self, key):
        # Find the appropriate leaf node
        leaf = self._find_leaf(self.root, key)

        # Avoid duplicate keys
        if key in leaf.keys:
            print(f"Key {key} already exists.")
            return

        # Insert key in sorted order
        index = bisect_left(leaf.keys, key)
        leaf.keys.insert(index, key)

        # If leaf does not overflow, insertion is complete
        if len(leaf.keys) < self.order:
            return

        # Split leaf if overflow occurs
        self._split_leaf(leaf)

    # ---------------------------------------------------------
    # FIND LEAF NODE
    # ---------------------------------------------------------
    def _find_leaf(self, node, key):
        current = node

        while not current.leaf:
            index = bisect_right(current.keys, key)
            current = current.children[index]

        return current

    # ---------------------------------------------------------
    # SPLIT LEAF NODE
    # ---------------------------------------------------------
    def _split_leaf(self, leaf):
        new_leaf = BPlusTreeNode(leaf=True)

        # Split approximately in half
        split_index = (len(leaf.keys) + 1) // 2

        new_leaf.keys = leaf.keys[split_index:]
        leaf.keys = leaf.keys[:split_index]

        # Maintain linked list of leaf nodes
        new_leaf.next = leaf.next
        leaf.next = new_leaf

        # First key of right leaf is copied to parent
        separator_key = new_leaf.keys[0]

        # If leaf is root
        if leaf == self.root:
            new_root = BPlusTreeNode(leaf=False)

            new_root.keys = [separator_key]
            new_root.children = [leaf, new_leaf]

            self.root = new_root
        else:
            # Find parent and insert separator
            parent = self._find_parent(self.root, leaf)

            self._insert_in_parent(
                parent,
                separator_key,
                leaf,
                new_leaf
            )

    # ---------------------------------------------------------
    # FIND PARENT NODE
    # ---------------------------------------------------------
    def _find_parent(self, current, child):
        if current.leaf:
            return None

        if child in current.children:
            return current

        for c in current.children:
            if not c.leaf:
                parent = self._find_parent(c, child)

                if parent is not None:
                    return parent

        return None

    # ---------------------------------------------------------
    # INSERT INTO PARENT
    # ---------------------------------------------------------
    def _insert_in_parent(self, parent, key, old_child, new_child):

        # Find position of old child
        child_index = parent.children.index(old_child)

        # Insert separator key
        parent.keys.insert(child_index, key)

        # Insert new child
        parent.children.insert(child_index + 1, new_child)

        # Check for overflow
        if len(parent.children) > self.order:
            self._split_internal(parent)

    # ---------------------------------------------------------
    # SPLIT INTERNAL NODE
    # ---------------------------------------------------------
    def _split_internal(self, node):
        new_internal = BPlusTreeNode(leaf=False)

        # Middle key is promoted to parent
        middle_index = len(node.keys) // 2
        promoted_key = node.keys[middle_index]

        # Keys after middle key go to new node
        new_internal.keys = node.keys[middle_index + 1:]

        # Children after middle key go to new node
        new_internal.children = node.children[middle_index + 1:]

        # Keep keys and children in old node
        node.keys = node.keys[:middle_index]
        node.children = node.children[:middle_index + 1]

        # If node is root
        if node == self.root:
            new_root = BPlusTreeNode(leaf=False)

            new_root.keys = [promoted_key]
            new_root.children = [node, new_internal]

            self.root = new_root

        else:
            # Find parent
            parent = self._find_parent(self.root, node)

            self._insert_in_parent(
                parent,
                promoted_key,
                node,
                new_internal
            )

    # ---------------------------------------------------------
    # DISPLAY TREE LEVEL BY LEVEL
    # ---------------------------------------------------------
    def display(self):
        if self.root is None:
            print("Tree is empty.")
            return

        queue = [self.root]
        level = 0

        print("\nB+ Tree:")

        while queue:
            next_queue = []

            print(f"Level {level}: ", end="")

            for node in queue:
                if node.leaf:
                    print("[", end="")

                    for i, key in enumerate(node.keys):
                        print(key, end="")
                        if i != len(node.keys) - 1:
                            print(", ", end="")

                    print("] ", end="")

                else:
                    print("<", end="")

                    for i, key in enumerate(node.keys):
                        print(key, end="")
                        if i != len(node.keys) - 1:
                            print(", ", end="")

                    print("> ", end="")

                    next_queue.extend(node.children)

            print()

            queue = next_queue
            level += 1

    # ---------------------------------------------------------
    # DISPLAY ALL KEYS USING LEAF LINKED LIST
    # ---------------------------------------------------------
    def display_leaves(self):
        current = self.root

        # Go to leftmost leaf
        while not current.leaf:
            current = current.children[0]

        print("\nKeys in sorted order:")

        while current is not None:
            for key in current.keys:
                print(key, end=" ")

            current = current.next

        print()


# =============================================================
# MAIN PROGRAM
# =============================================================

def main():

    print("==============================================")
    print("          B+ TREE IMPLEMENTATION")
    print("==============================================")

    # Order of B+ Tree
    order = int(input("Enter the order of B+ Tree (e.g., 4): "))

    if order < 3:
        print("Order should be at least 3.")
        return

    tree = BPlusTree(order)

    while True:

        print("\n----------------------------------------------")
        print("1. Insert")
        print("2. Search")
        print("3. Display B+ Tree")
        print("4. Display Keys in Sorted Order")
        print("5. Exit")
        print("----------------------------------------------")

        choice = input("Enter your choice: ")

        # -----------------------------------------------------
        # INSERT
        # -----------------------------------------------------
        if choice == "1":

            try:
                key = int(input("Enter key to insert: "))
                tree.insert(key)

                print(f"Key {key} inserted successfully.")

            except ValueError:
                print("Please enter a valid integer.")

        # -----------------------------------------------------
        # SEARCH
        # -----------------------------------------------------
        elif choice == "2":

            try:
                key = int(input("Enter key to search: "))

                if tree.search(key):
                    print(f"Key {key} found in B+ Tree.")
                else:
                    print(f"Key {key} not found in B+ Tree.")

            except ValueError:
                print("Please enter a valid integer.")

        # -----------------------------------------------------
        # DISPLAY TREE
        # -----------------------------------------------------
        elif choice == "3":
            tree.display()

        # -----------------------------------------------------
        # DISPLAY LEAF NODES
        # -----------------------------------------------------
        elif choice == "4":
            tree.display_leaves()

        # -----------------------------------------------------
        # EXIT
        # -----------------------------------------------------
        elif choice == "5":
            print("\nProgram terminated.")
            break

        else:
            print("Invalid choice. Please try again.")


# =============================================================
# PROGRAM EXECUTION
# =============================================================

if __name__ == "__main__":
    main()