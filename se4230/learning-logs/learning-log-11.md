- Question/Problem: Huffman project - How to  make a build-the-huffman-tree algorithm take O(k log k time) for k distinct symbols (using my Project 2 PriorityQueue)?
- When Identified: 10/16 6pm
- Importance: 5
- How to learn: Old code/projects (Project 2 PQ), hand-tracing a frequency table
- Insight/Answer:
    The O(k log k) comes entirely from the heap: every “find the two lightest nodes” step must be O(log k), not O(k).
    Count the operations: k leaves pushed, then k-1 merges. Each merge = 2 * (peek_min + remove) + 1 update, all O(log k). That's done k times, so O(k log k). The finished tree has exactly 2k-1 nodes (k leaves + k-1 internal).  
    - Merge = pop two, make Node(a.weight + b.weight, left=a, right=b), set both children’s .parent, push the new node. The last remaining node is the root  
    - Edge case: one distinct symbol would get a 0-bit code (undecodable), so hang it under a root as the 0-child to give it a 1-bit code  
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
    - Climb cost = depth = code length = bits emitted, so total time is O(output bits)  
    - Do NOT build a string with += or slice lists in a loop, since that hides an O(n) step inside the loop and makes the total quadratic  
    Decode: start at the root and take one edge per input bit (0 = left, 1 = right). On reaching a leaf, yield its symbol and jump back to the root. One step per bit, so O(input bits).  
    - Written as generators, so they accept any iterable and never copy the input
    - A bit stream that ends mid-code, or walks off the tree, means invalid input, so raise ValueError  
    Why not just a dictionary symbol → bit string? Space. Each entry has length = depth  
- Hours spent learning: 2
- Minutes spent documenting: 15
- Confidence: 4  

- Question/Problem: What is topological order?
- When Identified: 10/23 11am
- Importance: 5  
- How to learn: review with google & quiz question  
- Insight/Answer: "A DAG has the edges d→a, d→b, a→c, b→c. Which vertex must come first in every topological order?"    
    A topological order is a way of listing every vertex of a DAG so that for every edge u -> v, u appears BEFORE v (all goes forward). It only exists if the graph has no cycles (obviously).   
    => "d, since every other vertex has an edge coming into it"  
    d is the only vertex with no incoming edges (a and b each have one from d, c has two). Anything with an incoming edge must wait for its source, so only d can go first.  
    every other vertex coming in = they all go forward. this works because d has no outgoing edges too (otherwise, if it made a cycle back to, say, vertex a, that wouldn't be all forward)  
    - so this is pretty straightforward, I just didn't know the definition.  
    - but it was obviously not the alphabetical ordering option, I knew that much beforehand
- Hours spent learning: 1
- Minutes spent documenting: 10
- Confidence: 4


- Question/Problem: Implement the mini-lab practice without @cache?   
- When Identified: 10/23 11am
- Importance: 5  
- How to learn: review with google & can use C# or python with no caching imports   