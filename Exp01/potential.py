class DynamicArray:
    def __init__(self):
        self.capacity = 1
        self.arr = [None] * self.capacity
        self.size = 0
        self.old_phi = 0

    def insert(self, value):

        if self.size == self.capacity:
            actual = self.size + 1

            self.capacity *= 2
            new_arr = [None] * self.capacity

            for i in range(self.size):
                new_arr[i] = self.arr[i]

            self.arr = new_arr
        else:
            actual = 1

        self.arr[self.size] = value
        self.size += 1

        new_phi = 2 * self.size - self.capacity
        amortized = actual + (new_phi - self.old_phi)

        print("Inserted:", value)
        print("Actual Cost:", actual)
        print("Potential:", new_phi)
        print("Amortized Cost:", amortized)
        print("Array:", self.arr[:self.size])
        print()
        self.old_phi = new_phi

print("Potential Method")

d = DynamicArray()
for i in range(1, 9):
    d.insert(i)