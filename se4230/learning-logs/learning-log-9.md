- Question/Problem: Memoization & Fibonacci sequence  
- When Identified: 10/4 6pm  
- Importance: 4  
- How to learn: Textbook assigned section  
- Insight/Answer:  
    Refresh on the usual (naive) implementation of the Fibonacci sequence algorithm  
    ```
    if n = 0
        return 0
    else if n = 1  
        return 1  
    else  
        return fib(n-1) + fib(n-2)
    ```  
    The __memoization__ approach keeps a dictionary of computed values, F[n] as it recurses. This means it will never compute the same thing twice.
    ```
    if n = 0
        return 0
    else if n = 1  
        return 1  
    else  
        if F[n] is undefined  
            F[n] = fib(n-1) + fib(n-2)  
        return F[n]
    ```  
    F[n] is filled from the bottom up, starting with the first non-base case of F[2]. Thus, the evaluation of F_i only needs 1 evaluation per index i, making this have O(n) operations.  
    __"Fill Deliberately"__ (Iterative): same idea, but instead of needing the recursion calls to trigger the creation of F[n]: you can loop from 2 to n instead. At the end of that loop, the target F[n] would be the last element.  
- Hours spent learning: 1 
- Minutes spent documenting: 10  
- Confidence: 4   

- Question/Problem: Difference between memoization and dynamic programming (and why is the 'r' missing)?  
- When Identified: 10/4 12pm    
- Importance: 3
- How to learn: Textbook, Google. Find examples that highlight the difference between them.     
- Insight/Answer:  
    Memoization is from the idea of "memo", like a note-to-self. The idea is you keep a "memo" of a computed result to avoid computing it again.
  
    Memoization is ONE way to implement dynamic programming. Meanwhile, dynamic programming is a problem-solving PARADIGM.  
    Memoization is a technique about avoiding recomputes, and dynamic programming is an approach that makes use of "overlapping subproblems" and optimal substructure.
    _Memoization vs. Tabulation_: Top-down vs. Bottom-up dynamic programming.  
      - memoization: recurse down from the big problem  
      - tabulation: build up from the smallest subproblem
    __EXAMPLE__: Fibonacci  
    - Memoization: refer to the prior log about Fibonacci  
    - Tabulation: ironically, this is kind of how we intuitively solve the fibonacci by hand. Smallest subproblem IS when n < 2, and we work our way up until it's the target.  
      Ex: fib(4):
        - fib(0) = 0,
        - fib(1) = 1,
        - fib(2) = fib(prev) + fib(curr) = 0 + 1 = 1,
        - fib(3) = " = 2,  
        - fib(4) = " = 3
- Hours spent learning: 2/3 
- Minutes spent documenting: 5  
- Confidence: 3 

- Question/Problem: How does dynamic programming work on trees?  
- When Identified: 10/5 4pm    
- Importance: 4. Prelude to the project?  
- How to learn: Textbook 3.10  
- Insight/Answer: In previous examples, the structure used to make a memo on-- memoize-- had been arrays. Apparently, in tree problems, the structure is the tree itself.  
    __EXAMPLE__: Maximum Independent Set in a tree ; (independent set => a subset of vertices with no edges between them ; they may have EDGES to vertices outside the set, just not to each other). Premise: for a tree with n vertices, computing the largest independent set can be done in O(n) time.  
      
      Subproblems ARE the SUBTREES
      - MIS(v) = size of the largest independent set in the subtree rooted at v
      - Final Answer = MIS(root)  
      For each vertex, v, you can EITHER exclude or include v  
        - Exclude v → children are free: sum of MIS(child)
        - Include v → children are forbidden (they'd share an edge with v): 1 + sum of MIS(grandchild). We skip the children, basically.
      
      Memoization: store each MIS result as a field of each node itself, like v.MIS  
      MIS(v) depends on its children and grandchildren, so compute children BEFORE parents style of post-order traversal).  
      Leaves are the base case: MIS(leaf) = 1.
    **Why the tree is the table:** each node stores its own result (int: v.MIS); post-order gives a valid evaluation order for free, so recursion + node fields = memoization.  
    **Time O(n):** each vertex contributes constant work to its parent and grandparent only, so total work is O(n).  
    **Example:** A→{B, C}, B→{D, E}, C→{F}
    - Leaves D, E, F: yes=1, no=0
    - B: yes=1, no=2
    - C: yes=1, no=1
    - A: yes=1+2+1=4, no=max(1,2)+max(1,1)=3
    - Answer = 4, set = {A, D, E, F}   
- Hours spent learning: 5/4 
- Minutes spent documenting: 10  
- Confidence: 3 


- Question/Problem: How does 3SAT reduce to the Nonogram Puzzle?  
- When Identified: 10/2 12pm    
- Importance: 5
- How to learn: Consult Professor Teichert. It seems complicated enough that we were asked to "have an intuition" but a concrete, convincing proof probably is more complicated.    
