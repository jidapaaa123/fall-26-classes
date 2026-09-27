import pytest

# Part 1
def OptCost(start, end, frequencies):
    if start == end:
        return 0
    else:
        sum_freq = sum(frequencies[i] for i in range(start, end))

        best = None
        for root in range(start, end):
            cost_left = OptCost(start, root, frequencies)
            cost_right = OptCost(root + 1, end, frequencies)
            total = cost_left + cost_right
            if best is None or total < best:
                best = total

        return sum_freq + best


@pytest.mark.parametrize(
    "frequencies, expected_cost",
    [
        ([1, 2, 10], 17),          # A B C -> best tree roots at C, cost 17
        ([5], 5)
    ],
)
def test_opt_cost(frequencies, expected_cost):
    result = OptCost(0, len(frequencies), frequencies)
    assert result == expected_cost