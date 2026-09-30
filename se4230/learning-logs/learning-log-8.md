## Learning Log  

- Question/Problem: How do I implement penalty per search of left children in a Optimal BST problem?  
- When Identified: 9/22 6pm  
- Importance: 5  
- How to learn: test out my interpretation with steps of solving an example case (with values) until it agrees with the test cases  
- Insight/Answer:  
  In hindsight, the description was pretty clear: penalty *L* per search. The "per search" suggests this penaltied-cost will grow with frequency.  
  
  My first attempt was under the interpretation that *L* is charged per left turn according to the tree shape, independent of the search frequency  

  CORRECTION: frequency-dependent, so the expected cost (FROM the penalty alone) should be *L* * key_frequency. It's like the total cost at Node *A* is freq x depth (penalty-free) + freq x {turns to get there} x *L*.
  It's written this way because the entire subtree must already pass the current level (the penalty to get to the next level via a left-turn will get charged in its own recursion step): ```sum(frequencies[i] for i in range(start, root))```      
  **SOME EXTRAPOLATION CASES?**
  - **Right-turn penalty (or asymmetric L/R penalties)**: similar logic but with [root+1:end]  
  - **Alternating or path-dependent penalty (e.g. penalty doubles after two consecutive left turns)** - needs state-parameter passed through the recursion  
- Hours spent learning: 2  
- Minutes spent documenting: 5  
- Confidence: 3  

- Question/Problem: What is P vs. NP vs. NP-Hard vs. NP complete?  
- When identified: 9/23 11am  
- Importance: 5. Shouldn't be too bad as this is a re-organization from what was already discussed that forces me to process it.  
- How to learn: Google the differences  
- Insight/Answer:  
  NOTE: "Quickly" refers to something done in polynomial time, like $n^2, n^3, ... $  
  **DIFFERENCES**  
  P vs. NP problems: can both be verified quickly, but only P is guaranteed to "can be solved quickly"  
  NP vs. NP-Hard problems: NP-Hard is at least as hard as everything in NP, but we have no answer to if it's verified quickly  
  **ESSENTIAL QUESTIONS**: Can it be solved quickly? Can it be verified quickly?  
  P: Yes & Yes  
  NP: Unknown (yes for P, unknown for else) & Yes  
  NP-Hard: Believed no (at least as hard as everything in NP) & maybe, maybe not
  NP-Complete: Believed No & Yes (NP's verification, NP-Hard's "believed no")  
  **Reductions**: Difficulty is measured by reductions. For example, we can't prove the SAT problem needs exponential time, but we can prove it's as hard as every NP problem via reductions. This earns it the NP-Hard category  
  *Textbook*: "To prove that problem A is NP-hard, reduce a known NP-hard problem to A." Doing this means A is at least as hard as another NP-hard problem. (Reducing it to any NP problem does open the possibility of "maybe there's actually a harder NP problem that will not reduce to A").  
- Hours spent learning: 1  
- Minutes spent documenting: 5  
- Confidence: 4. The definitions and applications make sense. Reduction proofs are another conversation    
  
- Question/Problem: What is the 3Sat Problem and the Graph Coloring Problem?  
- When Identified: 9/23 6pm  
- Importance: 5   
- How to Learn: Textbook. Just enough to recognize what can reduce to it.  
- Insight/Answer:  
  **3SAT (from CircuitSAT)**  
  Like CircuitSAT in a sense that it's asking... 
    **QUESTION**: given an arbitrary circuit, is there an input assignment that makes the output true?  
  EXCEPT 3SAT is a _special case_ of SAT: the formula of interest is in conjunctive normal form (ANDed) of exactly 3 clauses (but each clause is however long). 
  NP-Hard proof by reducing CircuitSAT to it. (The proof that any SAT is NP-Hard is in Section 12.5 of the Textbook)  
  **Graph Coloring (from 3SAT)**  
    **QUESTION**: given a graph and a number *k*, can you properly color it with *k* colors?  
    For *k* >= 3, it's NP-complete  
  NP-Hard proof by reducing 3SAT to it  
  _Example of Graph Notation_:  G = (V, E) = (vertices, edges)  
    Triangle  
      V = {A, B, C}  
      E = {{A, B}, {B, C}, {A, C}}  
    So G = ({A, B, C}, {{A,B}, {B,C}, {A,C}}).  
    Square/Rectangle   
      V = {A, B, C, D}   
      E = {{A, B}, {B, C}, {C, D}, {D, A}}   
    So G = ({A, B, C, D}, {{A, B}, {B, C}, {C, D}, {D, A}}).   
    _NOTE - REDUCTION_: a reduction must preserve truth values (same exact answers/outputs as the reduced problem).  
    > Karp reduction makes 1 single call to, say, Problem B's solver. Turing/Cook reduction makes multiple calls to other Problems' solvers.   
    Ex (Karp reduction): Finding the minimum value in an unsorted list  
    - let Problem A = min(), Problem B = sort()  
    - we say A reduces to B because B's solver can be used to solve A: sorting the list, then find the identify first element in order to find the minimum value  
- Hours spent learning: 1  
- Minutes spent documenting: 5  
- Confidence: 3

- Question/Problem: How is any SAT problem NP-Hard?  
- When Identified: 9/27 6pm
- Importance: 2. I don't think this is pressing. It just seems like this is a ground fact that other proofs keep referring to  
- How to learn: Textbook 12.5 contains the proof   

- Question/Problem: How does 3SAT reduce to Circuit SAT? How does Graph Coloring reduce to 3SAT?  
- When Identified: 9/27 6pm
- Importance: 2.   
- How to learn: Textbook / Google / AI  