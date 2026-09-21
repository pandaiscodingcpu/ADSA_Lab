class DynamicArray:
    def __init__(self):
        self.capacity = 1
        self.arr = [None] * self.capacity
        self.size = 0
        self.credit = 0

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

        charged = 3
        self.credit = self.credit + charged - actual

        print("Inserted:", value)
        print("Actual Cost:", actual)
        print("Charged Cost:", charged)
        print("Credit:", self.credit)
        print("Array:", self.arr[:self.size])
        print()


d = DynamicArray()
for i in range(1, 9):
    d.insert(i)