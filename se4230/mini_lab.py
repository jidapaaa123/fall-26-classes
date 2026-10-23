# longest_from(graph, s) returns the number of edges on the longest path that
# starts at s in a DAG, where graph maps each vertex to the list of vertices
# its edges point to. (In the graph g below, s-a-c-t is one longest path.)
from functools import cache

def longest_from(g, start):
    @cache
    def longest_from_node(node):
        return max((1 + longest_from_node(child) for child in g[node]), default=0)
    return longest_from_node(start)

# def longest_from(g, start):
#     def longest_from_node(node, memo):
#         if node in memo:
#             memo[node] = max((1 + longest_from_node(child, memo) for child in g[node]), default=0)
#         return memo[node]
#     return longest_from_node(start, {})

def lis_length(values):
    @cache
    def longest_from(index):
        return 1 + max((
            longest_from(next_index) for next_index in range(index + 1, len(values)) 
            if values[next_index] > values[index])
            , default=0)
    return max((longest_from(i) for i in range(len(values))), default=0)



# Write it so that this pytest test passes in O(V + E) time:
g = {"s": ["a", "b"], "a": ["c", "t"], "b": ["c", "d"], "c": ["t"], "d": ["t"], "t": []}

def test_longest_from():
    assert longest_from(g, "s") == 3
    assert longest_from(g, "c") == 1
    assert longest_from(g, "t") == 0
    ladder = {i: [i + 1, i + 2] for i in range(60)} | {60: [], 61: []}
    assert longest_from(ladder, 0) == 60

# If you get done early, write lis_length(a), the length of the longest
# strictly increasing subsequence of the list a. Hint: it's a longest path in
# a DAG you never have to build. Make this pass in O(n^2) time:
def test_lis_length():
    assert lis_length([3, 1, 4, 1, 5, 9, 2, 6]) == 4
    assert lis_length([5, 4, 3]) == 1
    assert lis_length([]) == 0