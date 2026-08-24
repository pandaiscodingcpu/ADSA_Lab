# node definition
import random
class Node:
    # Every node in a skip list holds a value and an array of pointers (forward references) to the next nodes at different levels.
    def __init__(self,val,level):
        self.val = val
        # forward is an array of pointers to the next node at each level
        self.forward = [None] * (level + 1)

# definition of the skip list structure with p = 0.5 and max level = 16
class SkipList:
    def __init__(self,max_level=16,p=0.5):
        self.max_level = max_level
        self.p = p
        self.head = Node(None, self.max_level)
        self.level = 0  # Current highest level in the skip list

    def _random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def search(self, target):
        curr = self.head
        # Traverse downwards from the highest current level to level 0
        for i in range(self.level, -1, -1):
            while curr.forward[i] and curr.forward[i].val < target:
                curr = curr.forward[i]
        
        curr = curr.forward[0]
        if curr and curr.val == target:
            return True
        return False

    # insert function
    def insert(self,val):
        update = [None] * (self.max_level + 1)
        curr = self.head

        # Find position to insert across all levels
        for i in range(self.level,-1,-1):
            while curr.forward[i] and curr.forward[i].val < val:
                curr = curr.forward[i]
            update[i] = curr
        curr = curr.forward[0]

        # If value already exists, we can skip or update (here we skip duplicates)
        if curr is None or curr.val != val:
            r_level = self._random_level()

            # If random level is greater than current list level, initialize update pointers
            if r_level > self.level:
                for i in range(self.level + 1, r_level + 1):
                    update[i] = self.head
                self.level = r_level

            # Create new node and insert it by updating pointers
            new_node = Node(val, r_level)
            for i in range(r_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    # function to delete a node from the skip list
    def delete(self, val):
        update = [None] * (self.max_level + 1)
        curr = self.head

        # Find the node and record update pointers
        for i in range(self.level, -1, -1):
            while curr.forward[i] and curr.forward[i].val < val:
                curr = curr.forward[i]
            update[i] = curr

        curr = curr.forward[0]

        # If node exists, remove references
        if curr and curr.val == val:
            for i in range(self.level + 1):
                if update[i].forward[i] != curr:
                    break
                update[i].forward[i] = curr.forward[i]

            # Drop the list level if top levels are now empty
            while self.level > 0 and self.head.forward[self.level] is None:
                self.level -= 1
            return True
        return False


    # function to display
    def display(self):
        print("\n--- Skip List ---")
        for i in range(self.level, -1, -1):
            curr = self.head.forward[i]
            line = f"Level {i}: "
            while curr:
                line += f"{curr.val} -> "
                curr = curr.forward[i]
            print(line + "None")
        print("-----------------\n")


def main():
    skiplist = SkipList()
    while True:
        print("----- Skip List Operations----")
        print("1. Insert")
        print("2. Search")
        print("3. Delete")
        print("4. Display")
        print("5. Exit")
        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            val = int(input("Enter element: "))
            skiplist.insert(val)
            print("Element inserted successfully.")
        elif choice == 2:
            val = int(input("Enter element to search: "))
            if skiplist.search(val):
                print(f"Element {val} found.")
            else:
                print(f"Element {val} not found.")
        elif choice == 3:
            val = int(input("Enter element to delete: "))
            if skiplist.delete(val):
                print(f"Element {val} deleted successfully.")
            else:
                print(f"Element {val} not found in the skip list.")
        elif choice == 4:
            skiplist.display()
        elif choice == 5:
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()