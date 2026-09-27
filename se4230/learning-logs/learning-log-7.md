- Question/Problem: Practice examples of each case of the Master Theorem     
- When Identified: 9/19 11am   
- Importance: 5
- How to learn: Ask Claude to generate problems to solve of each case without labeling which question falls under which case. Do until I can refer to the Master Theorem instead of solving via recursion tree    
- Insight/Answer: Given form ```T(n) = a*T(n/b) + f(n^d)```. There are 3 cases, where we compare the a vs. b^d:  
  1) a < b^d: top-heavy  
    -> O(n^d)  
  2) a = b^d: balanced  
    -> O(n^d * log(n))  
  3) a > b^d: bottom-heavy  
    -> O(n^(log_b(a)))  
  This is the same notes I got from class/quiz. I just needed to spend time doing a few questions with BOTH Master Theorem & Recursion tree approaches so I feel comfortable using just the Master Theorem. I would save aside memorizing the rules for when there's a test in which I can't use notes... AND if time's really tight (because I still prefer the Recursion Tree approach)  
- Hours Spent Learning: 3/4  
- Minutes Spent documenting: 10  
- Confidence: 4  


- Question/Problem: How to solve recurrence where subproblem sizes are NOT divided?  
Ex: 2T(n-1) + O(n)  
- When identified: 9/21 11am  
- Importance: 3. I don't anticipate these to come up often.  
- How to learn: Attempt to solve it via a Recursion Tree. List assumptions made along the way & have Claude check against it
- Insight/Answer: So hopefully you don't run into these often because sometimes, summation identities are necessary and I really don't like those. I was able to write the summation, but I didn't separate the internal nodes vs. the leaves (so I just did 2^i*(n-i) for i=[0,n]). That wouldn't work because, at i=n, I would've received a 0 for work done at level n, which is NOT true: the base case (leaves) are NOT 0 work.  
  **WALKTHROUGH**  
  1) Total cost = internalNodes_cost + leaves_cost  
  2) $$\sum_{k=0}^{n-1} 2^k * (n-k)$$ $$ + 2^n * T(0)$$  
    - by magic of knowing, you can simplify the internal nodes summation via $$ j = n - k $$ 
    => $$\sum_{j=1}^{n} 2^{n-j} * j $$  
    => $$2^n\sum_{j=1}^{n} {j/2^j} $$  
    FACT: $$\sum_{j=1}^{\infty} {j/2^j} = 2$$, so
    => $$2^n * 2 = 2^{n+1}$$  
    ... which is basically the same thing as $\theta(2^n)$   
  3) TLDR: The leaves cost is 2^n * O(1) (we assume the base case does O(1) work here): 2^n. The summation of the internal nodes also equal out to be 2^n... so $\theta(2^n)$, ignoring constants  
  **Final Thoughts**:  
  - subproblem size via subtraction: always means LINEAR depth  
  - branching: 
    - a = 1 means the cost are linearly added, thus the resulting polynomial is 1 degree higher than the per-level work (*n* depth is a given, n nodes/levels * n^d per-level work each = n^(d+1))  
    - a > 1: theta(a^(n/b)). Because the number of leaves (due to a's branching) grows exponentially, while the per-level polynomial cost grows polynomially?  
- Hours spent learning: 2  
- Minutes spent documenting: 15  
- Confidence: 3  

- Question/Problem: What is backtracking?     
- When Identified: 9/20 12pm   
- Importance: 5  
- How to learn: Textbook 2.4 and 2.8 as assigned until I can articulate the book's points  
- Insight/Answer: "Backtrack = bruteforce + early abandonment/failure detection". (You recursively make decisions until you get to a base case, then 'undo' them.) Like, you search through every possible path (but abandon the path as soon as it you deduce the path is doomed). It's a bit different from bruteforce because it tries to 'abandon early', where if a path is doomed it will go back a step and try another option      
  **N-Queens Problem**: let n = 4. So 1820 options (16 choose 4)  
  1) Q1 in R1C1  
  2) Row 2: C1 & C2 are attacked, so put Q2 in R2C3  
  3) Row 3: every column is attacked. Still have Q3&Q4. Undo R2's choice in C3 and try the next option (only C4 is left)  
  3) Row 3: C1, C3, and C4 are attacked. Only option is putting Q3 in C2  
  4) Row 4: C1, C2, C3 and C4 are attacked. Deadend. We exhausted every option after picking C1 and R1, so undo all the way up to R1C1's choice  
  5) Repeat for Q1 in R1C2.  
  _Bruteforce difference_: Bruteforce would check all the 1820 options and verify, per each solution, that no queens are attacked.  

  **Subset Sum Problem**: "for each number, either include it or skip it." Once dead-end, undo to the last non-dead-end step and choose a different option.  
  Ex: [3, 5, 6, 7] to target = 9  
  1) Include 3; s = 3  
  2) Include 5; s = 8  
  3) Include 6; s = 14. ARGHHH! Go back (positive integers, so no hope of getting smaller)  
  4) s = 3; Exclude 5; s = 3  
  5) Include 6; s = 9. ARGHHH! (with joy). Solution.append([3, 6]). Go back and look for other solutions; we also know that [3,6] needs to be pruned because anything else will overshoot.  
  6) s = 3; Exclude 6; s = 3  
  7) Include 7; s = 10. ARGHHH!
  7) s = 3; Exclude 7; s = 3. ARGHHH! That's exhausted for the [3]'s tree.  
  8) Exclude 3; [5]... so on and so forth   
  _Bruteforce difference_: Bruteforce would check all 2^n subsets and verify that the subset sum equals the target.  

  **Optimal BST**  
  INTRO: A perfectly balanced tree might actually have a higher cost than an unbalanced one if, say, maybe a heavy-element is searched for more often.  
  Ex: [A B C] with frequency = [1 2 10]. C is the heaviest, so a balanced tree would put it at the bottom, like B -> [A C].  
    - cost = sum of (frequency * depth of node)  
           = 2x1 + 1x2 + 10x2  
           = 24 cost  
    vs. unbalanced tree, maybe C at the top: C -> B -> A  
    - cost = 10x1 + 2x2 + 1x3 = 17  
  SOLUTION: Try every key, *r*, as the root and build a proper BST.  
  cost(keys) = (sum of all freq.) + cost(left keys) + cost(right keys)
  Ex: 
  Root A: 13 + cost(empty) + cost(B, C).  
    - The best tree for {B, C} is C -> B, which costs 14 (1x10 + 2x2)  
    NOTE: 13 is from the fact that the subtree attaching to 1-level (from Root A) adds 1 more copy of its frequency due to 1 extra depth. C: 10x1 becomes 10x2 once attached; 10 extra cost, C: 2x2 becomes 2x3 once attached; 2 extra cost. 10 + 2 + 1 (from Root A) accounts for cost outside the subtree of interest  
  Root B: 13 + cost(A) + cost(C) = 13 + 1 + 10 = 24  
  Root C: 13 + cost(A, B) = 13 + 2 + 2 = 17  
  THUS Root C is the best option.  
  _Bruteforce difference_: Instead of generating every possible tree shape, we pick a root and pick the best left and right subtree for that root, then we know that's the best cost for the particular Root Choice. This approach also allows us to **cache the cost of the best subtree for a specific set of keys**  
- Hours spent learning: 2  
- Minutes spent documenting: 15  
- Confidence: 4  

- Question/Problem: Practice a few cases for subtraction-based subproblem recurrence.  
- When Identified: 9/21 10pm  
- Importance: 2. I don't expect a lot of these to actually show up? I'm just curious  
- How to learn: Have Claude generate a few exercises and solve it regularly, then compare against the "Guidelines" mentioned in the **Final Thoughts** section of LL7's entry about this.  