# Part 1: Theory and Implementation
## algorithms 
def bubble_sort(arr):
    if len(arr) == 0:
        return arr

    k=0
    for i in range(len(arr) - k):
        prev = arr[0]
        for j in range(len(arr)):
            curr = arr[j]
            if (prev > curr):
                arr[j] = prev
                arr[j-1] = curr
            else:
                prev = curr
            print(arr)
        k += 1
    return arr

def selection_sort(arr):
    if len(arr) == 0:
        return arr
    
    for i in range(len(arr)):
        print(f"{i+1} ITERATION")
        curr_smallest_index = i
        curr_smallest = arr[curr_smallest_index]
        for j in range(i, len(arr)):
            cand = arr[j]
            if (cand < curr_smallest):
                curr_smallest = cand
                curr_smallest_index = j
        tmp = arr[i]
        arr[i] = curr_smallest
        arr[curr_smallest_index] = tmp
        print(arr)
    return arr                

## pytests
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def add(a, b):
    return a + b

def test_bubble_sort():
    assert bubble_sort([]) == []
    arr = [23, 84, 23, 42, 91, 4, 55, 76, 12, 67]
    assert bubble_sort(arr) == [4, 12, 23, 23, 42, 55, 67, 76, 84, 91]
    arr1 = [3, 4, 1, 5, 2]
    assert bubble_sort(arr1) == [1, 2, 3, 4, 5]

def test_selection_sort():
    assert selection_sort([]) == []
    arr = [23, 84, 23, 42, 91, 4, 55, 76, 12, 67]
    assert selection_sort(arr) == [4, 12, 23, 23, 42, 55, 67, 76, 84, 91]
    arr1 = [3, 4, 1, 5, 2]
    assert selection_sort(arr1) == [1, 2, 3, 4, 5]
