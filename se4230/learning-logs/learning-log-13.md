- Question/Problem: What is the Max Flow Problem?   
- Insight/Answer:  
    Given a directed graph with edge capacities, a source `s`, and a sink `t`, find the most "stuff" that can be sent from `s` to `t`.  
    __A flow__ `f(e)` on each edge must satisfy:  
      - Capacity: `0 ≤ f(e) ≤ c(e)`  
      - Conservation: for every vertex except `s` and `t`, flow in = flow out  
    __Value of the flow__ = net flow leaving `s`. Max flow = the flow with the largest value.  
    __Min cut__: split the vertices into `S` (contains `s`) and `T` (contains `t`). Its capacity is the sum of capacities of edges going from `S` to `T` only. Edges going back from `T` to `S` don't count.  
    __Max-flow min-cut theorem__: max flow value = min cut capacity.  
    - Easy half: any flow must cross any cut, so flow value ≤ cut capacity for every cut  
    - So if you find a flow and a cut with the same number, both are optimal  
    __Integrality__: if all capacities are integers, some max flow uses integer flows on every edge. This is why max flow can model "count the paths" problems (matching, disjoint paths, Q4 below).  


- Question/Problem: Question 4 of Chapter 11 Zombie City  
- Insight/Answer:  
    __Ford-Fulkerson__ (greedy with an undo button):  
    ```
    f = 0 on every edge
    while there is a path s → t in the residual graph:
        b = smallest residual capacity on that path (bottleneck)
        push b along the path (update the residual graph)
    return total flow pushed
    ```  
    __Connection to cuts__: when the loop stops, no path from `s` to `t` exists in the residual graph.  
      - Let `S` = all vertices reachable from `s` in the residual graph, `T` = the rest (so `t` is in `T`)  
      - Every original edge `S → T` must be saturated (full), otherwise its residual edge would let us reach more vertices  
      - Every original edge `T → S` must have zero flow, otherwise its backward residual edge would point from `S` to `T`  
      - So flow value = capacity of cut `(S, T)`. Since no flow can beat any cut, **both are optimal**  
      - This is the proof of max-flow min-cut, and it gives an algorithm to find the min cut: run the flow, then search from `s` in the residual graph  
    __Running time__:  
      - Each augmentation is O(E) (one BFS/DFS). With integer capacities, each augmentation adds at least 1, so at most `|f*|` rounds: **O(E · |f*|)**  
      - Can be slow if capacities are huge and paths are chosen badly. Edmonds-Karp (always pick the shortest path by BFS) gives **O(V · E²)** regardless of capacities  


- Question/Problem: Ford-Fulkerson algorithm? what's that anything to do with cuts?  
- Insight/Answer:  
    A residual graph shows **how much more flow each edge could take, and how much could be undone**.  
    For each original edge `u → v` with capacity `c` and current flow `f`:  
      - Forward edge `u → v` with residual capacity `c − f` (room left), kept only if > 0  
      - Backward edge `v → u` with residual capacity `f` (flow that can be cancelled), kept only if > 0  
    Pushing flow along a backward edge means **reducing** flow on the original edge.  
    __Why backward edges are needed__: without them, a bad early choice gets stuck.  
    Example: `s→a`, `s→b`, `a→b`, `a→t`, `b→t`, all capacity 1. Max flow is 2.  
      - Greedy picks `s→a→b→t` (flow 1). Now `s→a`, `a→b`, `b→t` are full, and no forward path remains  
      - The residual graph has a backward edge `b→a`. The path `s→b→a→t` exists and uses it, which cancels `a→b`  
      - Result: `s→a→t` and `s→b→t`, flow 2  
    __Notes__:  
      - Residual graph edges can go in directions the original graph doesn't have  
      - The min cut is read from the residual graph: vertices reachable from `s` at the end are the `S` side  


- Question/Problem: What are residual graphs?  
- Insight/Answer:  
    This is a **minimum vertex cut** between `s` and `t`. Reduce it to max flow by making **vertices** the things with capacity.  
    __Construction__ (vertex splitting):  
    1. Replace every vertex `v` other than `s`, `t` with two vertices `v_in` and `v_out`, joined by an edge `v_in → v_out` of capacity **1** (closing the station costs 1)  
    2. For every undirected rail edge `{u, v}`, add **two** directed edges: `u_out → v_in` and `v_out → u_in`, each with capacity **∞** (rail lines can't be "closed", only stations)  
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
