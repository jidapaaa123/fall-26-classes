(- Question/Problem: Un-rust Big O Analysis Skills Pt. 2  
- When Identified: 9/2 11am
- How to Learn: Emphasis on Quick Sort and Counting Sort. Review the sorting algorithms again: try to guess best/worst/average case scenario.)  

(- Question/Problem: What are the 'siblings' of Big-O (concept)?  
- When Identified: 9/2 11am)  

- Question/Problem: Understand difference between Big O vs. Omega vs. Theta in practice  
- When Identified: 9/4 11am 

(- Question/Problem: How do I write sorting algorithms that require partitioning?  
- When Identified: 9/3 6pm)

(- Question/Problem: How do I convince myself Merge Sort is O(n*log(n))?  
- When Identified: 9/3 6pm)  

- Question/Problem: How do I visually represent my graph (in Python)?  
- When Identified: 9/8 6pm  

- Question/Problem: "... the minimum spanning tree and the shortest path tree are not the same" How come ?    
- When Identified: 9/9 6pm  

- Question/Problem: Is it recommended to use mutable objects as default INITAL VALUES in Python class FIELDS?  
- When Identified: 9/11 12am    
- Importance:
- Insight/Answer: NO.  

- Question/Problem: Analyze Prim's Algorithm implementation  
- When Identified: 9/12 12am    
- Importance:
- How to learn: implement Graph/PQ such that it works on its own but NOT with Prim's Algorithm?  


- Question/Problem: Chapter 1 exercises Question 9  
- When Identified: 9/21 12pm  
- Importance: 3  
- How to learn: Try to come up with my own answers. Check them against Claude's until I can articulate it.  

(- Question/Problem: Practice a few cases for subtraction-based subproblem recurrence.  
- When Identified: 9/21 10pm  
- Importance: 2. I don't expect a lot of these to actually show up? I'm just curious  
- How to learn: Have Claude generate a few exercises and solve it regularly, then compare against the "Guidelines" mentioned in the **Final Thoughts** section of LL7's entry about this.)  

- Question/Problem: Understand the recurrence problems in Quiz 2  

(- Question/Problem: How does 3SAT reduce to the Nonogram Puzzle?  
- When Identified: 10/2 12pm    
- Importance: 5
- How to learn: Consult Professor Teichert. It seems complicated enough that we were asked to "have an intuition" but a concrete, convincing proof probably is more complicated.    )

(- Question/Problem: Review minimum spanning tree and (greedy) Prim's algorithm.  
- When Identified: 10/13 6pm     
- Importance: 5  
- How to learn: Google   )

(- Question/Problem: What is the Max Flow Problem?   
- Question/Problem: Ford-Fulkerson algorithm? what's that anything to do with cuts?  
- Question/Problem: What are residual graphs?  )

- Question/Problem: I need a simple documentation of how residual graphs are constructed to refer back to quickly.  
https://claude.ai/chat/d8b4c0c4-98fc-44f1-ab39-d82d770cf0a5 "How does one construct a residual graph then?"

- Question/Problem: Question 4 of Chapter 11 Zombie City  
(- Insight/Answer:  
    This is a **minimum vertex cut** between `s` and `t`. Reduce it to max flow by making **vertices** the things with capacity.  
    __Construction__ (vertex splitting):  
    1. Replace every vertex `v` other than `s`, `t` with two vertices `v_in` and `v_out`, joined by an edge `v_in -> v_out` of capacity **1** (closing the station costs 1)  
    2. For every undirected rail edge `{u, v}`, add **two** directed edges: `u_out -> v_in` and `v_out -> u_in`, each with capacity **∞** (rail lines can't be "closed", only stations)  
    3. Source = `s`, sink = `t` (not split, since they can't be closed)  
    4. Run max flow. The answer = max flow value  
    __Why it works__:  
      - Every path from `s` to `t` passes through station edges (capacity 1). A cut of finite capacity can only cut those edges, never the ∞ rail edges, so a finite cut = a set of stations whose closing blocks all paths  
      - Min cut = max flow, so min stations = max flow value  
      - Equivalently (Menger's theorem): min stations to close = max number of paths from `s` to `t` that share no station besides `s` and `t`  
    __Finding which stations to close__: after max flow, search from `s` in the residual graph. Close each `v` where `v_in` is reachable but `v_out` is not.  
    __Edge case__: if `s` and `t` are directly connected, no set of closures can block them. Return "impossible" (the ∞ edge makes max flow infinite).  
    __Running time__: the new graph has about `2V` vertices and `V + 2E` edges. The answer is at most `V − 2`, so Ford-Fulkerson does at most `V` augmentations of O(E) each: **O(V · E)**.  
    __Check on the example__: two red stations separate `s` from `t`, and there are 2 station-disjoint paths from `s` to `t`, so the flow is 2. ✓  
    __Why ∞ and not 1 on rail edges__: with capacity 1 the min cut could cut a rail edge instead of a station. That would count the wrong thing (and can't be undone by closing a station when the edge touches `s` or `t`).
)

(

- Question Problem: How to reduce Nonogram to LP? For the "most efficient" part of the solver for Step 5 of final project  

- When identified: 11/16 11am  

- Importance: 5. Building on my understanding of ILP. Even if I generally grasp ILP, I still need to apply it to the context and constraints of the Nonogram game/puzzle  

- How to learn: I wonder if someone's thought this already for SAT. I feel Nonogram and SAT are really similar so I can draw inspo from how someone reduced Nonogram to ILP.  
)  

(- Question/Problem: Question 4 of Chapter 11 Zombie City. The big huddle is thoroughly understand max flow enough to reduce any problem to it... it's not a direct problem. I HAVE TO "REDUCE IT." And at point of discovery I didn't understand max flow beyond its name and goal 

- When identified: 11/1 6pm 

- Importance: 5. I need to submit this 

- How to learn: Mostly, I googled how to reduce a problem to a max flow problem. This is a hot topic on forums that care about graph theory in general. It said something about needing an edge to cut. 

- Insight/Answer: TBA )

