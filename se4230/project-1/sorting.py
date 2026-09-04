import pytest
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
        k += 1
    return arr

def selection_sort(arr):
    if len(arr) == 0:
        return arr
    
    for i in range(len(arr)):
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
    return arr                

def insertion_sort(arr):
    return arr        

## pytests
@pytest.mark.parametrize("alg", [bubble_sort, selection_sort, insertion_sort], ids=lambda f: f.__name__)
def test_mega_sort(alg):
    arr = [23, 84, 23, 42, 91, 4, 55, 76, 12, 67]
    sorted_arr = [4, 12, 23, 23, 42, 55, 67, 76, 84, 91]
    arr1 = [3, 4, 1, 5, 2]
    sorted_arr1 = [1, 2, 3, 4, 5]

    copy_arr = arr.copy()
    copy_arr1 = arr1.copy()
    assert alg(copy_arr) == sorted_arr
    assert alg(copy_arr1) == sorted_arr1
