# Name: Jidapa Angsutti
# Course: SE 4230
# Date: 9/2/2026
# Run [python -m pytest sorting.py] to run the tests
# Run [python sorting.py] to run the benchmark. Output updates the sort_times.png & sort_times.csv

import pytest
import random
import time
import statistics
import pandas as pd
import seaborn as sns

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
    print("NEW LEVEL")
    if len(arr1) > 1:
        arr1 = root_merge_sort(*split_in_half(arr1))
    if len(arr2) > 1:
        arr2 = root_merge_sort(*split_in_half(arr2))

    copy_arr1 = arr1.copy()
    copy_arr2 = arr2.copy()
    
    tmp = []
    while len(copy_arr1) + len(copy_arr2) > 0:
        print(f"{copy_arr1} vs. {copy_arr2}")
        arr_to_pop = array_with_smaller_min(copy_arr1, copy_arr2)
        popped = arr_to_pop.pop(0)
        tmp.append(popped)
        print(tmp)
        
    print(f"{arr1} + {arr2} => {tmp}")
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
    
## pytests
my_sorts = [merge_sort]
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

    negatives = [-3, 5, -1, 0, -8]
    sorted_negatives = [-8, -3, -1, 0, 5]

    all_negative = [-5, -1, -9, -3]
    sorted_all_negative = [-9, -5, -3, -1]
    
    inputs = [empty, single, 
              two_elements_sorted,
              two_elements_unsorted, 
              already_sorted, reverse_sorted, 
              all_duplicates, some_duplicates, 
              negatives, all_negative]
    outputs = [sorted_empty, sorted_single, 
               sorted_two_elements_sorted, 
               sorted_two_elements_unsorted, 
               sorted_already_sorted, 
               sorted_reverse_sorted, 
               sorted_all_duplicates, 
               sorted_some_duplicates, 
               sorted_negatives, 
               sorted_all_negative]
    
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
   timeout = 0.01
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