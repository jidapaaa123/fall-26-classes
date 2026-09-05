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
        print(f"Curr: {curr}, i: {i}")
        print(arr)
        if curr < prev:
            print(f"It need swap")
            root_insertion_sort(arr, i)
            print(arr)
    return arr



def swap_elements(arr, i, j):
    tmp = arr[i]
    arr[i] = arr[j]
    arr[j] = tmp

## pytests
my_sorts = [bubble_sort, selection_sort, insertion_sort]
@pytest.mark.parametrize("alg", my_sorts, ids=lambda f: f.__name__)
def test_mega_sort(alg):
    arr = [23, 84, 23, 42, 91, 4, 55, 76, 12, 67]
    sorted_arr = [4, 12, 23, 23, 42, 55, 67, 76, 84, 91]
    arr1 = [3, 4, 1, 5, 2]
    sorted_arr1 = [1, 2, 3, 4, 5]

    copy_arr = arr.copy()
    copy_arr1 = arr1.copy()
    assert alg(copy_arr) == sorted_arr
    assert alg(copy_arr1) == sorted_arr1

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