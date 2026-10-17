- Question/Problem: Huffman project - How to  make a build-the-huffman-tree algorithm take O(k log k time) for k distinct symbols (using my Project 2 PriorityQueue)?
- When Identified: 10/16 6pm
- Importance: 5
- How to learn: Old code/projects (Project 2 PQ), hand-tracing a frequency table
- Insight/Answer:
    The O(k log k) comes entirely from the heap: every “find the two lightest nodes” step must be O(log k), not O(k).
    Count the operations: k leaves pushed, then k-1 merges. Each merge = 2 × (peek_min + remove) + 1 update, all O(log k). Total = (k + 3(k-1)) × O(log k) = O(k log k). The finished tree has exactly 2k-1 nodes (k leaves + k-1 internal).
    Why the data structure matters (alternatives I checked):
    - Re-sort the list before every merge: still optimal, but O(k² log k) (k-1 sorts of up to k items)
    - Quickselect for the 2 smallest every merge: still optimal, but O(k²) expected, O(k³) worst case
    - Sort once, then keep merging the running result with the next symbol: WRONG, not just slow. Counterexample (a,1) (b,1) (c,1) (d,1): Huffman cost 8 (all depth 2) vs chain cost 9
    How I used my PriorityQueue:
    - The PQ needs unique, hashable keys, but symbols’ frequencies can tie and merged nodes have no symbol. So the key = an integer id (next_id, incremented per push), the priority = weight, and the data slot holds the tree Node
    - Merge = pop two, make Node(a.weight + b.weight, left=a, right=b), set both children’s .parent, push the new node. The last remaining node is the root
    - Edge case: one distinct symbol would get a 0-bit code (undecodable), so hang it under a root as the 0-child to give it a 1-bit code
    Cost check: total cost = Σ freq × depth = sum of the weights of all internal nodes (each frequency is counted once per ancestor, i.e. depth times). Hand-trace of a=3, b=8, c=10, d=14, e=17, f=42 gave code lengths 1,3,3,3,4,4 and cost 209
- Hours spent learning: 2
- Minutes spent documenting: 15
- Confidence: 4

- Question/Problem: Huffman project - How to make encode/decode take time proportional to the number of bits, and why store the tree + symbol→leaf map instead of a symbol→bitstring dictionary?
- When Identified: 10/16 8pm
- Importance: 5
- How to learn: Hand-tracing the tree, Google
- Insight/Answer:
    The Codec stores the tree (nodes with left, right, parent) plus a hash map symbol → leaf node. That one structure supports both directions in O(bits).
    Encode: for each symbol, look up its leaf in O(1), then climb .parent pointers to the root, recording 0 if I came from the left child and 1 if from the right. Reverse that list to get root-to-leaf order and yield it.
    - Climb cost = depth = code length = bits emitted, so total time is O(output bits) (the reverse doubles the work but stays proportional)
    - Do NOT build a string with += or slice lists in a loop, since that hides an O(n) step inside the loop and makes the total quadratic
    Decode: start at the root and take one edge per input bit (0 = left, 1 = right). On reaching a leaf, yield its symbol and jump back to the root. One step per bit, so O(input bits).
    - Written as generators, so they accept any iterable and never copy the input
    - A bit stream that ends mid-code, or walks off the tree, means invalid input, so raise ValueError
    Why not just a dictionary symbol → bit string? Space. Each entry has length = depth, so the dictionary costs Σ depth:
    - Balanced tree: about k log k
    - Skewed tree (Fibonacci-like frequencies make a caterpillar with depths 1, 2, …, k-1): about k²/2 = O(k²)
    - Tree + symbol→leaf map: 2k-1 nodes with O(1) data each, plus k pointers = O(k) always. The tree stores each edge once and every code sharing that prefix reuses it
    Tradeoff: getting a symbol’s bits from the tree takes O(depth) instead of an O(1) lookup, but I save space and the same tree is also what decoding walks down.
- Hours spent learning: 2
- Minutes spent documenting: 15
- Confidence: 4