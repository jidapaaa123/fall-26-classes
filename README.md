# fall-26-classes
temp repo for my classes for now i guess

# alg project 11/21
## Correctness of the SAT -> ILP Reduction

**Construction.** For a CNF formula f with n distinct variables, m clauses, and L literal occurrences, build an ILP with all variables binary:

- `x_v` for each SAT variable v  
- `n_v = 1 − x_v` for each variable that appears negated  
- For each clause, a left-to-right chain of OR gates over its literal variables  
- A left-to-right chain of AND gates, ending in `out`  
- The constraint `out = 1`  

Gate constraints:
- **OR:** `o ≥ a`, `o ≥ b`, `o ≤ a + b`
- **AND:** `x ≤ a`, `x ≤ b`, `x ≥ a + b − 1`
- **NOT:** `n = 1 − a` .
o, x, n are {0,1} as well if a, b are {0,1}


### 1. Polynomial time: the reduction (the construction of the ILP instance from f) runs in time polynomial in the size of f.  

The ILP has at most n input variables, n NOT variables, L − m OR-gate variables, and m − 1 AND-gate variables. n + n + L - m + m - 1 = 2n + L - 1 variables.  
Each NOT adds 1 constraint, each gate adds 3, and the final `out = 1` adds 1, so there are n + 3L - 2 constraints.   
Both runtime for making variables and constraints are O(L).  
Each variable and constraint is created with constant work, so the whole construction takes O(L) time. The translation is considered cheap if it's polynomial   

### 2. SAT-satisfiable implies ILP-feasible:

Let S satisfy f.  
SAT variable v.  

- Set `x_v = 1` iff S(v) is true, and `n_v = 1 − x_v`.  
- For each gate: look at its 2 inputs to compute the boolean output 0/1. (Say ILP variable o1 = x_a v x_b & a = 1, you compute o1 = 1). With the rules we set (o >= a, o >= b, o <= a+b>) in the problem construction, our ILP constraints/values are compatible with this boolean computation.  
- Each literal's ILP-variable-representation (Ex: x_v) equals that literal's truth value (Ex: v) under S. So an OR gate over the variables == OR over the truth values. Thus we can say `c_j` equivalently represents clause j's value.  
- Our rule for AND gate also holds. So with S, every clause c_j is 1: `out = 1` as all its 1-inputs become AND-ED.  

So every constraint holds and the ILP is feasible.  

### 3. ILP-feasible implies SAT-satisfiable:

Take any feasible solution. All variables are binary. 
Define S(v) = true iff `x_v = 1`.  

- For a positive literal v, its variable x_v is 1 iff S(v) is true, by the definition of S. For a negated literal not_v, the constraint n_v = 1 − x_v makes n_v equal to 1 iff x_v = 0 iff S(v) is false iff not_v is true. So every literal's variable equals that literal's truth value under S.  
- Every gate constraint holds with binary inputs, so by the lemma each gate variable equals its boolean gate value.  
- By induction, `c_j = 1` iff some literal of clause j is true under S, and `out = 1` (after AND-ing all c_j) iff every `c_j = 1` .
- The constraint `out = 1` therefore forces every clause to contain a true literal, so S satisfies f.  