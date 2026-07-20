class DynamicArray:
    def __init__(self) -> None:
        self.current = 0   
        self.capacity = 1    
        self.array = [0] * self.capacity 

    def push(self, item):
        cost = 1
        if self.current == self.capacity:
            cost += self.current 
            new_capacity = self.capacity * 2
            new_array = [0] * new_capacity
            for i in range(self.current):
                new_array[i] = self.array[i]
                
            self.array = new_array
            self.capacity = new_capacity
        self.array[self.current] = item
        self.current += 1
        return self.capacity, cost
    
    
if __name__ == "__main__":
    try:
        n = int(input("Enter the number of elements to push: "))
    except ValueError:
        print("Please enter a valid integer.")
        exit()
        
    d = DynamicArray()
    print(f"\n{'Item':<8}{'Size':<12}{'Cost':<6}")
    print("-" * 28)
    total_cost = 0
    for i in range(1, n + 1):
        capacity, cost = d.push(i)
        size_cap_str = f"{capacity}"
        
        print(f"{i:<8}{size_cap_str:<12}{cost:<6}")
        total_cost += cost
    print(f"Average cost: {total_cost / n}")