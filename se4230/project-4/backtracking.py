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