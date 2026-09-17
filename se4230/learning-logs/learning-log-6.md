# Learning Log  
- Question/Problem: What is Karatsuba's method and why's it such a big deal?  
- When identified: 9/16 11am
- Importance: 5  
- How to learn:  Youtube'd & Quora'd  
- Insight/Answer: TLDR - FOIL identities allow you to do 3 multiplications + 1 subtraction instead of 4 multiplications  
    (Ex: 1243*5678)
    Problem: traditional multiplication of numbers of number of size n and number of size m requires n*m single-digit multiplications
    ==> (1200+43)(5600+78) FOIL 
    = 10^4(12*56) + 10^2(12*78 + 43*56) + 43*78  
    --> 16 single-digit multiplications
    Solution (12 single-digit multiplications):  
    1) Recognize that the product is 10^4(ac) + 10^2(ad+bc) + bd  
      - thus, the Needed Parts are [ac ad bc bd]
    2) Recognize that (a+b)(c+d) = ac + ad + bc + bd and derive:  
       (a+b)(c+d) - ac - bd = ad + bc   
    3) Recognize these parts:  
      - P1 = ac  
      - P2 = bd  
      - P3 = (a+b)(c+d) ==> ac + ad + bc + bd
      - middle term = P3 - P1 - P2  
         because  
         = ac + ad + bc + bd - ac - bd  
         = ad + bc   
    4) Realize: you only need to multiply P1, P2, and P3 to get all the Needed Parts. Subtraction is cheap  
    5) Use P1 P2 and P3 to solve for  
      1243 * 5678 = (100a+b)(100c+d)
                  = 10^4(ac) + 10^2(ad+bc) + (bd)  
      where a = 12, b = 43, c = 56, d = 78  
- Hours Spent: 1  
- Minutes spent: 10
- Confidence: 4  

- Question/Problem: Big O of Karatsuba?     
- When Identified: 9/14 11am  
- Importance: 3  
- How to Learn: try to guess then Google
- Insight/Answer:  
  - Per level: split into 3 multiplications, each of size n/2 numbers -> 3* T(n/2)
  - Per level: 
    - 2 additions: a+b, c+d  O(n)  
    - 2 additions: P3 - P1 - P2  O(n)  
    - shifts of powers of 10  O(n)  
  - Therefore recurrence T(n) = 3*T(n/2) + O(n)  
Level 0: 1 problem of size n, total cost n
Level 1: 3 problems of size n/2, total cost = 3*n/2  
Level 2: 9 problems of size n/4, total cost = 9*n/4  
Level k: 3^k problems of size n/2^k, total cost = 3^k/(n/2^k) = n*(3/2)^k  
==> bottom-heavy  
Sub-problem size is 1 when k = log_2(n) because  
n/2^k = 1; k = log_2(n)  
Bottom-heavy at level k = log_2(n)  
So most of the work is at that level k = log_2(n):  
n*(3/2)^(log_2(n)) 
Use log identity ==> 3^log_2(n) / n = n^(log_2(3))  
- Hours Spent: 0.5  
- Minutes spent: 10  
- Confidence: 3  




- Question/Problem: Review Proof by Induction  
- When Identified: 9/16 11am  
- Importance: 3
- How to learn: book  
- Insight/Answer:  
  - Pre-review: Isn't it just proving 2 things: the base case, say P(1), and then prove that if P(n) is true, then P(n+1) is true?  
  - Only ways to prove a universally quantified statement: 1) direct proof OR 2) contradiction  
  
  Example: 'Every integer greater than 1 has a prime divisor.' -> proof by contradiction  

  So apparently that counts as induction too. 
  - Post-review: it seems that induction, at its core, is about building off given assumptions. I need more practice to execute them, but reading them backwards in hindsight isn't too hard to understand (about 55% of the time)  
- Hours spent: 2/3  
- Minutes spent: 5
- Confidence: 2  
 


- Question/Problem: Some examples in which, in T(n) notation, the non-recursive part is NOT O(1)?    
- When Identified: 9/14 10am  
- Importance: 2  
- How to learn: Claude ask
- Insight/answer: So we actually got this on accident by studying Karatsuba. So here are some other examples, hopefully patterns emerge.  
  - O(1) -> choosing, comparing  
  - O(n^d) where d > 0 -> having to touch every element?  
  Ex: Merge Sort has + O(n) => when you're merging every item from the 2 stacks at a time
  Ex: Karatsuba + O(n) (see above) => shifting, adding, subtracting   
  Ex: Quicksort has + O(n) => re-arranging according to the pivot  
  ==> having to touch every element... I mean obviously. I think I'll just need more exposure if I want to be able to design an algorithm with a specific kind of non-recursive work on the spot    
- Hours spent: 0.5 
- Minutes spent: 10  
- Confidence: 3
