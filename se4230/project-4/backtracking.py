import pytest

# # Part 1
# def opt_cost(start, end, frequencies):
#     if start == end:
#         return 0

#     total = sum(frequencies[i] for i in range(start, end))
#     best = None
    
#     for root in range(start, end):
#         left = opt_cost(start, root, frequencies)
#         right = opt_cost(root + 1, end, frequencies)
#         candidate = left + right
#         if best is None or candidate < best:
#             best = candidate

#     return total + best


# def cost(frequencies):
#     if not frequencies:
#         return 0
#     return opt_cost(0, len(frequencies), frequencies)

# Part 2
def cost(frequencies):
    if not frequencies:
        return 0
    
    def opt_cost(start, end):
        if start == end:
            return 0

        total = sum(frequencies[i] for i in range(start, end))
        best = None
        
        for root in range(start, end):
            left = opt_cost(start, root)
            right = opt_cost(root + 1, end)
            candidate = left + right
            if best is None or candidate < best:
                best = candidate

        return total + best

    return opt_cost(0, len(frequencies))

# Part 3
def combine_costs_and_trees(root_info, left_info, right_info):
    # info = (cost, "tree")
    root_cost, root = root_info
    left_cost, left = left_info
    right_cost, right = right_info
    return (root_cost + left_cost + right_cost, (root, left, right))


def cost_and_tree(frequencies):
    if not frequencies:
        return 0, ()

    def opt_cost_and_tree(start, end):
        if start == end:
            return 0, ()

        root_cost = sum(frequencies[i] for i in range(start, end))

        best = None
        for root in range(start, end):
            candidate = combine_costs_and_trees(
                (root_cost, root),
                opt_cost_and_tree(start, root), # left subtree info
                opt_cost_and_tree(root + 1, end), # right subtree info
            )
            if best is None or candidate[0] < best[0]:
                best = candidate

        return best

    return opt_cost_and_tree(0, len(frequencies))

# --- Parts 1 and 2: the cost alone ------------------------------------------

@pytest.mark.parametrize("frequencies,expected", [
    ([5], 5),
    ([4, 3], 10),
    ([1, 1, 1], 5),
    ([10, 1, 1, 1, 1], 22),
    ([1, 2, 3, 4, 5], 30),
    ([4, 3, 28, 100, 5], 190),
    ([7, 2, 9, 1, 3, 8], 58),
    ([3, 1, 4, 1, 5, 9, 2], 53),
])
def test_optimal_cost(frequencies, expected):
    assert expected == cost(frequencies)


def test_empty_library_costs_nothing():
    assert 0 == cost([])
    
# --- Part 3: the cost and the tree ------------------------------------------
# Each of these has exactly one optimal tree, so there is a single right answer.

@pytest.mark.parametrize("frequencies,expected", [
    ([5], (5, (0, (), ()))),
    ([4, 3], (10, (0, (), (1, (), ())))),
    ([1, 1, 1], (5, (1, (0, (), ()), (2, (), ())))),
    ([4, 3, 28, 100, 5], (190, (3, (2, (0, (), (1, (), ())), ()), (4, (), ())))),
    ([7, 2, 9, 1, 3, 8], (58, (2, (0, (), (1, (), ())), (5, (4, (3, (), ()), ()), ())))),
])
def test_optimal_cost_and_tree(frequencies, expected):
    assert expected == cost_and_tree(frequencies)