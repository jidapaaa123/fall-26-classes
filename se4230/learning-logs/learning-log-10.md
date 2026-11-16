- Question/Problem: How to implement an optimal BST solution with penalty rules via dynamic programming (Project)?  
- When Identified: 10/7 6pm     
- Importance: 5  
- How to learn: Old code/projects & Google  
- Insight/Answer: 
      Same tree-shaped DP as before, but the subproblems are contiguous RANGES of bins, and the "penalty rules" (rotation, movement, scan costs) enter as extra STATE.  

    __Subproblem__: `best_subtree_cost(lo, hi, pos, facing_positive)` = min cost for all requests whose bin is in `[lo, hi)`, given the robot is at `pos` facing a direction.  
      - `pos` is always the parent's bin (just outside the range), so it adds only a constant number of states per range
      - Direction MUST be in the state: it decides whether the next move pays a rotation. Without it, the memoized answers are wrong.  
      - Final answer = `best_subtree_cost(0, n, 0, False)` (robot starts at bin 0 facing negative)  
    __Recurrence__: try every `r` in `[lo, hi)` as root.  
    cost(r) = W * (rotate + move + scan)         # every request in range pays the root step once
        + freq[r] * deliver                  # requests ending at r: (rotate if facing positive) + r * move_cost
        + best(lo, r, r, d) + best(r+1, hi, r, d)   # left/right subtrees, d = heading after reaching r  
    - `W = sum(freq[lo:hi])`: each step of a request's path is charged once, at the node where it happens  
    - Base case: empty range (`lo >= hi`) returns 0  
    - Left child always needs a negative heading, right child always positive  
    - `r == pos` only occurs at the top-level call (no move, no rotation)  
    __Memoization__: `@cache` on the nested function (all args hashable). Backtracking alone is exponential and never finishes for 50 bins.            
- Hours spent learning: 2   
- Minutes spent documenting: 15   
- Confidence: 4    

- Question/Problem: How do memoization tools like functools.lru_cache and functools.cache work under the hood? How are they different?  
- When Identified: 10/7 6pm     
- Importance: 2. Just curious  
- How to learn: Google / Python documentation   
- Insight/Answer:       
    Both are decorators that wrap a function with a dictionary: key = the call's arguments, value = the return value. On a call, look up the key; on a hit, return the stored value and skip the function body. On a miss, run the function, store the result, return it
    __Under the hood__:  
      - Arguments are packed into a key tuple, then hashed. So all args MUST be hashable (ints, bools, tuples OK; lists, dicts, sets NOT).  
      - `f(1, 2)` and `f(a=1, b=2)` can be cached as different keys, so call style should be consistent.  
      - The cache lives on the wrapper function (one per decorated function). A nested function decorated inside another function gets a FRESH cache on every call of the outer function, so results don't leak between inputs.  
    __Difference__:  
      - `functools.cache` = unbounded. Never evicts, so memory grows with the number of distinct calls. Equivalent to `lru_cache(maxsize=None)`. Simpler and a bit faster since there's no eviction bookkeeping.  
      - `functools.lru_cache(maxsize=128)` = bounded. Once full, it evicts the Least Recently Used entry (tracked with a linked list so each access is O(1)). Default size is 128. Can also set `maxsize=None` to make it unbounded.  
      - `lru_cache` can also use `typed=True` to cache `f(3)` and `f(3.0)` separately.  
- Hours spent learning: 1   
- Minutes spent documenting: 10   
- Confidence: 3     

- Question/Problem: What is the Huffman coding / Algorithm?  
- When Identified: 10/10 6pm     
- Importance: 5  
- How to learn: Relevant sections on the textbook / Google     
- Insight / Answer: https://www.youtube.com/watch?v=0uCnBiy3Wuw  
  Basically, it uses the same idea from the optimal BST problem: "more popular elements should be easier to access == closer to the top / root".   
    Huffman coding is **lossless compression**: give each symbol a binary code, so frequent symbols get SHORT codes and rare ones get LONG codes. Fewer total bits than fixed-length codes (e.g. 8 bits/char).  
    __Goal__: minimize total cost = sum of `freq[s] * depth(s)` over all symbols. Same shape as the optimal BST cost (frequency x depth), but here we pick the tree shape freely (it's not a binary tree).  
    __Prefix-free codes__: no codeword is a prefix of another, so the bit stream decodes unambiguously with no separators. Achieved by putting symbols at the LEAVES of a binary tree: left edge = `0`, right edge = `1`, and the path from root to a leaf is that symbol's code.  
      - Depth of a leaf = code length, so "popular == near the root" is literally "popular == short code"  
    __Algorithm (greedy, not DP)__: 
    put every symbol in a min-heap keyed by frequency  
    while heap has more than 1 node:
      a = pop min; b = pop min
      push new node (freq = a.freq + b.freq, children a, b)
      return the last node (the root)  
      - Repeatedly merge the two LEAST frequent nodes, so the rarest symbols end up deepest  
      - Decoding: walk the tree bit by bit from the root; at a leaf, output the symbol and restart at the root  
- Hours spent learning:  2  
- Minutes spent documenting: 15   
- Confidence: 3      

- Question/Problem: Review minimum spanning tree and (greedy) Prim's algorithm.  
- When Identified: 10/13 6pm     
- Importance: 5  
- How to learn: Google   