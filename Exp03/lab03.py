# randomized quick sort
import random

def left(arr,low,high):
    pivot = arr[high]
    i = low
    for j in range(low,high):    
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[high] = arr[high], arr[i]
    return i
def right(arr,low,high):
    r = random.randint(low,high)
    arr[r], arr[high] = arr[high], arr[r]
    return left(arr, low, high)

def quicksort(arr,high,low):
    if low < high:
        p = right(arr,low,high)
        quicksort(arr,low,p-1)
        quicksort(arr,p+1,high)
def display(arr):
    for element in arr:
        print(element, end=" ")
    print()
arr = [6, 4, 12, 8, 15, 16]
n = len(arr)
print("Original array:", end=" ")
display(arr)
quicksort(arr, 0, n - 1)
print("Sorted array:", end=" ")
display(arr)
