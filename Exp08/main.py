class IntervalNode:

  def __init__(self, low, high):
    self.low = low
    self.high = high
    self.max = high
    self.left = None
    self.right = None


class IntervalTree:

  def __init__(self):
    self.root = None

  def insert(self, root, low, high):
    """Inserts a new interval into the tree."""
    if root is None:
      return IntervalNode(low, high)

    if low < root.low:
      root.left = self.insert(root.left, low, high)
    else:
      root.right = self.insert(root.right, low, high)

    if root.max < high:
      root.max = high

    return root

  def add_interval(self, low, high):
    self.root = self.insert(self.root, low, high)

  def _do_overlap(self, l1, h1, l2, h2):
    return l1 <= h2 and l2 <= h1

  def search(self, root, low, high):
    """Searches for an overlapping interval."""
    if root is None:
      return None

    if self._do_overlap(root.low, root.high, low, high):
      return (root.low, root.high)

    if root.left is not None and root.left.max >= low:
      return self.search(root.left, low, high)

    return self.search(root.right, low, high)

  def find_overlap(self, low, high):
    return self.search(self.root, low, high)

  def display_tree(self, root, level=0, prefix="Root: "):
    """Displays the interval tree hierarchically."""
    if root is not None:
      print(" " * (level * 4) + prefix + f"[{root.low}, {root.high}] (max: {root.max})")
      if root.left is not None or root.right is not None:
        if root.left:
          self.display_tree(root.left, level + 1, "L--- ")
        else:
          print(" " * ((level + 1) * 4) + "L--- None")
        
        if root.right:
          self.display_tree(root.right, level + 1, "R--- ")
        else:
          print(" " * ((level + 1) * 4) + "R--- None")


if __name__ == "__main__":
  tree = IntervalTree()

  default_intervals = [(15, 20), (10, 30), (17, 19), (5, 20)]
  for l, h in default_intervals:
    tree.add_interval(l, h)

  while True:
    print("\n--- Interval Tree Operations ---")
    print("1. Insert an Interval")
    print("2. Search for an Overlapping Interval")
    print("3. Display Tree Structure")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ").strip()

    match choice:
      case "1":
        try:
          low = int(input("Enter interval low value: "))
          high = int(input("Enter interval high value: "))
          if low > high:
            print("Error: 'low' cannot be greater than 'high'.")
            continue
          tree.add_interval(low, high)
          print(f"Successfully inserted [{low}, {high}]")
        except ValueError:
          print("Invalid input. Please enter valid integers.")

      case "2":
        try:
          low = int(input("Enter query interval low value: "))
          high = int(input("Enter query interval high value: "))
          result = tree.find_overlap(low, high)
          if result:
            print(f"Overlap found! Query [{low}, {high}] overlaps with stored interval {result}")
          else:
            print(f"No overlapping intervals found for [{low}, {high}].")
        except ValueError:
          print("Invalid input. Please enter valid integers.")

      case "3":
        print("\nCurrent Interval Tree Structure:")
        if tree.root is None:
          print("Tree is empty.")
        else:
          tree.display_tree(tree.root)

      case "4":
        print("Exiting")
        break

      case _:
        print("Invalid choice! Please enter a number between 1 and 4.")