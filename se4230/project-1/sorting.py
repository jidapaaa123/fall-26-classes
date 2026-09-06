# Name: Jidapa Angsutti
# Course: SE 4230
# Date: 9/2/2026
# Run [python -m pytest sorting.py] to run the tests
# Run [python sorting.py] to run the benchmark. Output updates the sort_times.png & sort_times.csv

# NOTE: I wrote the pytest to assume the algorithm RETURNS the sorted list
# Even if the algorithm could sort it in-place, I just kept it that way anyway
# In-place implementations have "return arr" where arr IS the input array

import pytest
import random
import time
import statistics
import pandas as pd
import seaborn as sns
import random

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

# i = index to check for swaps
def root_insertion_sort(arr, i):
    if i == 0:
        return arr
    if arr[i] < arr[i-1]:
        swap_elements(arr, i, i-1)
        root_insertion_sort(arr, i-1)
    return arr

def insertion_sort(arr):
    if len(arr) == 0 or len(arr) == 1:
        return arr
    
    for i in range(1, len(arr)):
        curr = arr[i]
        prev = arr[i-1]
        if curr < prev:
            root_insertion_sort(arr, i)
    return arr

def swap_elements(arr, i, j):
    tmp = arr[i]
    arr[i] = arr[j]
    arr[j] = tmp

def root_merge_sort(arr1, arr2):
    if len(arr1) > 1:
        arr1 = root_merge_sort(*split_in_half(arr1))
    if len(arr2) > 1:
        arr2 = root_merge_sort(*split_in_half(arr2))

    copy_arr1 = arr1.copy()
    copy_arr2 = arr2.copy()
    
    tmp = []
    i = j = 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            tmp.append(arr1[i])
            i += 1
        else:
            tmp.append(arr2[j])
            j += 1
    tmp.extend(arr1[i:])
    tmp.extend(arr2[j:])
        
    return tmp
    
    
def merge_sort(arr):
    if len(arr) == 0 or len(arr) == 1:
        return arr

    (half1, half2) = split_in_half(arr)
    sorted = root_merge_sort(half1, half2)
    
    return sorted

def split_in_half(arr):
    midpoint = len(arr) // 2
    return (arr[:midpoint], arr[midpoint:])
    
def array_with_smaller_min(arr1, arr2):
    if len(arr1) == 0 and len(arr2) == 0:
        raise ValueError("supposedly this should not even be called?")
    if len(arr1) == 0:
        return arr2
    if len(arr2) == 0:
        return arr1  
    
    min1 = arr1[0]
    min2 = arr2[0]
    arr1_picked = min1 <= min2
    return (arr1 if arr1_picked else arr2)


# low/high = min/max of unsorted subarray
def quicksort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low >= high:
        return arr

    pivot_index = random.randint(low, high)
    # move pivot away from the unsorted subarray
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    pivot = arr[high]

    boundary = low
    for i in range(low, high):
        if arr[i] < pivot:
            arr[i], arr[boundary] = arr[boundary], arr[i]
            boundary += 1
    # GUARANTEE: left of the boundary = < pivot
    # GUARANTEE: right of boundary = >= pivot
    # there4: pivot should be at the boundary
    arr[boundary], arr[high] = arr[high], arr[boundary]

    # process the less-than and greater-than halves
    quicksort(arr, low, boundary - 1)
    quicksort(arr, boundary + 1, high)
    
    return arr

def counting_sort(arr):
    if len(arr) <= 1:
        return arr

    arr_max = max(arr)
    # make room for 0 (assignment says integers are between 0-1023)
    # ex: [1, 2, 4] -> [0, 0, 0, 0, 0]
    occurrences = [0] * (arr_max + 1)      
    for num in arr:
        # num = 1 -> goes in index 1
        occurrences[num] += 1
    
    prefix_sums = [0] * (arr_max + 1)      
    prefix_sums[0] = occurrences[0]
    for i, val in enumerate(occurrences[1:]):
        prefix_sums[i+1] = val + prefix_sums[i]
    # prefix sum val at index i MEANS
    # the last occurrence of value 'i' should be placed
    # BEFORE index val
    # think: prefix sum of 0 is 2 and of 1 is 3. So [0, 0, 1]
    # last '0' is placed before index 2.

    output = [0] * len(arr)
    for num in arr:
        p_sum = prefix_sums[num]
        output[p_sum-1] = num
        prefix_sums[num] -= 1
    
    return output

## pytests
my_sorts = [bubble_sort, selection_sort, insertion_sort, merge_sort, quicksort, counting_sort]
@pytest.mark.parametrize("alg", my_sorts, ids=lambda f: f.__name__)
def test_mega_sort(alg):
    empty = []
    sorted_empty = []

    single = [42]
    sorted_single = [42]

    two_elements_sorted = [1, 2]
    sorted_two_elements_sorted = [1, 2]

    two_elements_unsorted = [2, 1]
    sorted_two_elements_unsorted = [1, 2]

    already_sorted = [1, 2, 3, 4, 5]
    sorted_already_sorted = [1, 2, 3, 4, 5]

    reverse_sorted = [5, 4, 3, 2, 1]
    sorted_reverse_sorted = [1, 2, 3, 4, 5]

    all_duplicates = [7, 7, 7, 7, 7]
    sorted_all_duplicates = [7, 7, 7, 7, 7]

    some_duplicates = [3, 1, 2, 3, 1]
    sorted_some_duplicates = [1, 1, 2, 3, 3]
    
    inputs = [empty, single, 
              two_elements_sorted,
              two_elements_unsorted, 
              already_sorted, reverse_sorted, 
              all_duplicates, some_duplicates, 
              ]
    outputs = [sorted_empty, sorted_single, 
               sorted_two_elements_sorted, 
               sorted_two_elements_unsorted, 
               sorted_already_sorted, 
               sorted_reverse_sorted, 
               sorted_all_duplicates, 
               sorted_some_duplicates, 
               ]
    
    for i in range(len(inputs)):
        copy_input = inputs[i].copy()
        assert alg(copy_input) == outputs[i]

# control functions
def built_in_sorted(a):
   a[:] = sorted(a)

def in_place_sort(a):
   a.sort()

def do_nothing(a):
   pass

def make_two_copies(a):
   return list(a) * 2

def quadratic_garbage(a):
   for i in range(len(a)):
      for j in range(len(a)):
            a[i], a[j] = a[j], a[i]

def reverse_sorted(a):
   return list(reversed(sorted(a)))

def unchanged(a):
   return a

# I excluded some because they kind of cluttered up the graph later
# control_group = [built_in_sorted, in_place_sort, do_nothing, make_two_copies, quadratic_garbage]
control_group = [built_in_sorted, quadratic_garbage]

# Part 2: Empirical benchmark
def time_sort(original, prep, sort):
   a = prep(list(original))
   start = time.perf_counter()
   sort(a)
   end = time.perf_counter()
   return end - start

def aggregated_time_sort(lists, length, prep, sort, repetitions):
   return statistics.median(
      [time_sort(a[:length], prep, sort)
            for a in lists
            for _ in range(repetitions)])

sorts = [*my_sorts, *control_group]
if __name__ == '__main__':
   random.seed(4567)
   preps = [sorted, reverse_sorted, unchanged]
   num_lengths = 7
   length_base = 10
   max_value = 2 ** 10
   max_length = length_base ** (num_lengths - 1)
   random_lists = [[random.randint(0, max_value) for _ in range(max_length)] for _ in range(3)]
   lengths = [length_base**k for k in range(num_lengths)]
   repetitions = 3
   timeout = 1
   results = []
   
   for prep in preps:
      print(f'\n{prep.__name__}')
      for sort in sorts:
            print(f'\n\t{sort.__name__}', end='')
            for length in lengths:
               median_time = aggregated_time_sort(lists=random_lists, length=length,
                                             prep=prep, sort=sort, repetitions=repetitions)
               print('.',end='')
               results.append(dict(
                  sort=sort.__name__,
                  prep=prep.__name__,
                  length=length,
                  time=median_time))
               if median_time > timeout:
                  # don't consider longer lists if it already was too long on this one
                  break
   print()
   print(results)
   pd.DataFrame(results).to_csv("sort_times.csv")
   
sns.set_theme()
data = pd.read_csv("sort_times.csv")
plot = sns.relplot(data=data, kind='line', x='length', y='time', style='prep', hue='sort', palette='tab10', markers=True, dashes=True)
plot.savefig("sort_times.png")