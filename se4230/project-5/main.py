import sys
from functools import cache

# PART 2
def optimal_cost_backtracking(
    frequencies,
    cost_per_rotation,
    move_cost_per_distance,
    cost_per_scan,
):
    R = cost_per_rotation
    M = move_cost_per_distance
    S = cost_per_scan
    n = len(frequencies)

    def best_subtree_cost(lo, hi, pos, facing_positive):
        if lo >= hi:
            return 0

        W = sum(frequencies[lo:hi])  # the sum(all_freq_in_range) cost to account for root-level
        best = float("inf")

        # for every candidate root...
        for r in range(lo, hi):
            if r == pos:  # only possible at the top-level call (pos = r = 0)
                d_pos = facing_positive
                rotate = 0
                move = 0
            else:
                d_pos = r > pos
                rotate = R if d_pos != facing_positive else 0
                move = abs(r - pos) * M

            # Requests that find their target at r: 
            ## turn to face negative if currently positive, 
            ## then go home (move r units).
            deliver = (R if d_pos else 0) + r * M

            cost = (
                W * (rotate + move + S) # EVERY request (in range) pays this subtree's root step once. The root step incurs rotate, move, and scan cost
                + frequencies[r] * deliver  # deliver cost * expecting_this_many_deliveries
                + best_subtree_cost(lo, r, r, d_pos) # cost for requests whose bin in left subtree
                + best_subtree_cost(r + 1, hi, r, d_pos) # " in right subtree
            )
            best = min(best, cost)

        return best

    return best_subtree_cost(0, n, 0, False)

# PART 3
def optimal_cost_memoized(
    frequencies,
    cost_per_rotation,
    move_cost_per_distance,
    cost_per_scan,
):
    R = cost_per_rotation
    M = move_cost_per_distance
    S = cost_per_scan
    n = len(frequencies)

    sys.setrecursionlimit(max(sys.getrecursionlimit(), 10 * n + 1000))
    prefix = [0]
    for f in frequencies:
        prefix.append(prefix[-1] + f) # prefix[i] = sum of the first i freqs

    @cache
    def best_subtree_cost(lo, hi, pos, facing_positive):
        if lo >= hi:
            return 0

        W = prefix[hi] - prefix[lo]  # the sum(all_freq_in_range) cost to account for root-level
        best = float("inf")
        # it's == sum(frequencies[lo:hi]) by way of what the cache represents 
        
        # for every candidate root...
        for r in range(lo, hi):
            if r == pos:  # only possible at the top-level call (pos = r = 0)
                d_pos = facing_positive
                rotate = 0
                move = 0
            else:
                d_pos = r > pos
                rotate = R if d_pos != facing_positive else 0
                move = abs(r - pos) * M

            # Requests that find their target at r: 
            ## turn to face negative if currently positive, 
            ## then go home (move r units).
            deliver = (R if d_pos else 0) + r * M

            cost = (
                W * (rotate + move + S) # EVERY request (in range) pays this subtree's root step once. The root step incurs rotate, move, and scan cost
                + frequencies[r] * deliver  # deliver cost * expecting_this_many_deliveries
                + best_subtree_cost(lo, r, r, d_pos) # cost for requests whose bin in left subtree
                + best_subtree_cost(r + 1, hi, r, d_pos) # " in right subtree
            )
            best = min(best, cost)

        return best

    return best_subtree_cost(0, n, 0, False)

# PROVIDED TESTS
# (frequencies, rotation, move, scan, optimal cost, optimal tree)
# Each case has exactly one optimal tree, so the tree is safe to check.
OPTIMAL_BST_CASES = [
    ([5],                3, 1, 2,   10, (0, (), ())),
    ([4, 3],             3, 1, 2,   44, (0, (), (1, (), ()))),
    ([4, 30],            3, 1, 2,  348, (1, (0, (), ()), ())),
    ([1, 1, 1],          3, 1, 2,   30, (0, (), (1, (), (2, (), ())))),
    ([4, 3, 28, 100, 5], 3, 1, 2, 2072, (3, (2, (1, (0, (), ()), ()), ()), (4, (), ()))),
    ([1, 1, 1, 1, 1, 50], 7, 2, 1, 1940,
     (5, (4, (3, (2, (1, (0, (), ()), ()), ()), ()), ()), ())),
    ([3, 1, 4, 1, 5, 9, 2, 6], 5, 2, 3, 1132,
     (2, (1, (0, (), ()), ()),
         (5, (4, (3, (), ()), ()), (7, (6, (), ()), ())))),
    ([20, 5, 1, 1, 30, 2, 2, 40], 4, 1, 0, 1512,
     (0, (), (1, (), (2, (), (3, (), (4, (), (5, (), (6, (), (7, (), ()))))))))),
]

# Fifty bins. Only a memoized solution finishes this one -- plain backtracking would
# have to look at more trees than there are atoms in anything you care about.
FIFTY_BIN_FREQUENCIES = (4, 3, 28, 100, 5) * 10
FIFTY_BIN_COST = 96532


def test_backtracking_finds_the_optimal_cost():
    for frequencies, rotation, move, scan, cost, tree in OPTIMAL_BST_CASES:
        assert cost == optimal_cost_backtracking(
            frequencies, cost_per_rotation=rotation, move_cost_per_distance=move, cost_per_scan=scan
        ), frequencies


def test_memoized_finds_the_same_costs():
    for frequencies, rotation, move, scan, cost, tree in OPTIMAL_BST_CASES:
        assert cost == optimal_cost_memoized(
            frequencies, cost_per_rotation=rotation, move_cost_per_distance=move, cost_per_scan=scan
        ), frequencies


def test_memoized_handles_fifty_bins():
    assert FIFTY_BIN_COST == optimal_cost_memoized(
        list(FIFTY_BIN_FREQUENCIES), cost_per_rotation=3, move_cost_per_distance=1, cost_per_scan=2)


def test_optimal_tree_and_its_cost():
    for frequencies, rotation, move, scan, cost, tree in OPTIMAL_BST_CASES:
        assert (cost, tree) == optimal_tree(
            frequencies, cost_per_rotation=rotation, move_cost_per_distance=move, cost_per_scan=scan
        ), frequencies


def test_optimal_tree_still_works_on_fifty_bins():
    frequencies = list(FIFTY_BIN_FREQUENCIES)
    cost, tree = optimal_tree(
        frequencies, cost_per_rotation=3, move_cost_per_distance=1, cost_per_scan=2)
    assert FIFTY_BIN_COST == cost
    # every bin appears exactly once, and the tree is a search tree on the bin numbers
    def bins_in_order(t):
        return [] if t == () else bins_in_order(t[1]) + [t[0]] + bins_in_order(t[2])
    assert list(range(len(frequencies))) == bins_in_order(tree)


if __name__ == "__main__":
    # Runs the tests without pytest, so you can step through them in a debugger.
    for test in [test_backtracking_finds_the_optimal_cost,
                 test_memoized_finds_the_same_costs,
                 test_memoized_handles_fifty_bins,
                 test_optimal_tree_and_its_cost,
                 test_optimal_tree_still_works_on_fifty_bins]:
        test()
        print("passed:", test.__name__)