- Question/Problem: What is the Max Flow Problem? I KNOW it's about maximizing what can be pushed through, but not really about the terms or, specifically, the "cut".  
- When identified: 11/4 11am      
- Importance: 5; I just don't get any of it  
- How to learn: Relevant textbook sections, Youtube. Specifically ones that answer what a cut is referring to; a general overview/terminology tour is sufficient for this specific log  
- Insight/Answer:  
    Given a directed graph with edge capacities, a source `s`, and a sink `t`, find the most "stuff" that can be sent from `s` to `t` (& the path to get there).  
    __A flow__ `f(e)` on each edge must satisfy:  
      - Capacity: `0 ≤ f(e) ≤ c(e)` ; c(e) = capacity of edge ; f(e) = flow, how much actually to pass through  
      - Conservation: for every vertex except `s` and `t`, flow in = flow out. NO STORING AT AN EDGE - that's not a thing    
    __Value of the flow__ = net flow leaving `s`. Max flow = the flow with the largest value out of all the possible path options.  
    __Min cut__: split the vertices into `S` (contains `s`) and `T` (contains `t`). Its capacity is the sum of capacities of edges going from `S` to `T` only (inter-cut). Edges going back from `T` to `S` don't count. So, say we have nodes s,a,b,t with Cut S = {s,a}, T = {b,t} with edges: s->b (4), a->t (3), b->a (10). The cut capacity is 4 + 3, without counting the b->a. (This example isn't necessarily the min-cut though)    
    __Max-flow min-cut theorem__: max flow value = min cut capacity.  
    - Min-cut: it's relly about picking a partition (what to be in S's team, what to be in T's team. Point blank) and the min-cut value is that inter-partition capacity. Pick the partitioning with minimum value 
    - Min-cut provides the ceiling for what max flow could be. In the above example, the min-cut is 3 via S = {s, a, b} T = {t}: a->t (3). That means if you found a path with max flow 3, rest assured there is no path with max flow 4.  
Hours Spent learning: 2  
Minutes spent documenting: 15  
Confidence: 4. With respect to the purpose defined, yes, I do get the terminology, "cut" and how max-flow min-cut is used to deduce the answer.  

- Question/Problem: What are residual graphs? Is there only one residual graph per any given flow graph? I keep hearing about it in explanations related to Max Flow.   
- When identified: 11/6 6pm  
- Importance: 3. I have an inkling that researching Ford-Fulkerson will indirectly have me using a residual graph. But I'd like to know it as an independent definition/concept just because
- How to learn: Google, Youtube. Resources that can answer how a residual graph is meant to be used    
- Insight/Answer:  
    A residual graph shows **how much more flow each edge could take, and how much could be undone**.  
    For each original edge `u -> v` with capacity `c` and current flow `f`:  
      - Forward edge `u -> v` with residual capacity `c − f` (room left), kept only if > 0. "  
      - Backward edge `v -> u` with residual capacity `f` (flow that can be cancelled), kept only if > 0.  
    Pushing flow along a backward edge means **reducing** flow on the original edge.  
    __Why backward edges are needed__: without them, a bad early choice gets stuck. This is our undoing tool    
    Example: `s->a`, `s->b`, `a->b`, `a->t`, `b->t`, all capacity 1. Max flow is 2.  
      - Greedy picks `s->a->b->t` (flow 1). Now `s->a`, `a->b`, `b->t` are full, and no forward path remains  
      - The residual graph has a backward edge `b->a`. The path `s->b->a->t` exists and uses it, which cancels `a->b`  
      - Result: `s->a->t` and `s->b->t`, flow 2  
    __Notes__:  
      - Residual graph edges can go in directions the original graph doesn't have  
      - TLDR: okay. It's actually just like an alter-ego of the distribution-of-flows graph, I understand?  
- Hours spent learning: 1  
- Minutes spent documenting: 15  
- Confidence: 4. Unless I'm wrong, it's just like a graph to reference when making augmentation decisions  

- Question/Problem: Ford-Fulkerson algorithm? I know it's use to find max flow. But what else? And what does it entail?     
- When identified: 11/4 11am  
- Importance: 5. This was brought up in class often... and videos of it seems to follow an intuitive process? That said I need to understand it enough to implement it in code, not just an intuitive by-hand solving  
- How to learn: Videos showing examples of solving via Ford-Fulkerson.  
- Insight/Answer:  
    __Ford-Fulkerson__ (greedy with an undo button): it gives you the maximum flow (both the flow path & the value) & a min-cut (if you do BFS on s on the final residual graph).  
    ```
    f = 0 on every edge
    while there is a path s -> t in the residual graph:
        b = smallest residual capacity on that path (bottleneck)
        push b along the path (update the residual graph)
    return total flow pushed
    ```  
    __EXAMPLE__: 
    Problem setup: 2 bread factories. They ship through 2 hubs to deliver to city with...  
      s -> F1 (10): Factory 1 can bake 10 breads/day  
      s -> F2 (8): Factory 2 can bake 8 breads/day  
      F1 -> H1 (6): F1-to-H1 road can fit 6 breads/day  
      F1 -> H2 (5): That but with different nodes & capacities  
      F2 -> H2 (4): "
      H1 -> t: Hub 1 can deliver 7/day to the city (sink)  
      H2 -> t: "  
      Goal: most loaves per day that can reach the city?  
      Method: Max flow (that's why it's here). Ford-Fulkerson tells how to move through the paths and the max value from it  
      Steps:  
      Each round finds a path of edges with residual > 0 and pushes the bottleneck (aka the smallest residual on the path)  
      I suggest updating the residual graph per step to keep up (the table already documents the flow & I don't think we need more visualizations)  
      Round | Path | Residuals on path | Bottleneck | Total 
      -----------------------------------------------------
      1 | s->F1->H1->t | 10 6 7 | 6 | 6  
      2 | s->F2->H2->t | 8 4 6 | 4 | 10 
      3 | s->F1->H2->t | 4 5 2 | 2 | 12  
      Now for round 4, we find only a few residual edges > 0.  
          s->F1 = 2 residual ; F1->H2 = 3 residual ; H2->t = 0 residual. This path is blocked ; F1->H1 = 0, also blocked  
          Backward edge? H2->F2 = 4 capacity "up to 4 loaves of flow on this path can be cancelled/decremeneted". (forward edge, residual = can flow this much more; backward edge, leftover capacity = can take back this much) This is not helpful because: then F2 has to deal with <= 4 loaves. Those loaves can only go to H2, because that's the only place F2 links to.  
          "You can move forward along an edge that still has room, or backward along an edge that already carries something"
      This fulfills a termination for the algorithm: "can the search from `s` reach `t` using any residual edge, forward or backward?" No, we cannot.   
      Max Flow Value = 12  
      Min-cut: S = {s,F1,F2,H2}, T={H1,t}  
        "BFS on the final residual graph":  
        Same logic of "You can move forward along an edge that still has room, or backward along an edge that already carries something"
        s->F1->H2. Can't go to t, because H2->t = 0. Can backward to F2 (but cuz it's BREADTH-FS, see below:)  
        s->F2 (F2 already reached). Can't go to H2, but it's also already reached via another path anyway. Changes nothing  
- Hours spent learning: 4  
- Minutes spent documenting: 20  
- Confidence: 4.  
          
- Question/Problem: Question 4 of Chapter 11 Zombie City. The big huddle is thoroughly understand max flow enough to reduce any problem to it... it's not a direct problem. I HAVE TO "REDUCE IT." And at point of discovery I didn't understand max flow beyond its name and goal      
- When identified: 11/1 6pm   
- Importance: 5. I need to submit this  
- How to learn: Mostly, I googled how to reduce a problem to a max flow problem. This is a hot topic on forums that care about graph theory in general. It said something about needing an edge to cut. 
- Insight/Answer: TBA  
