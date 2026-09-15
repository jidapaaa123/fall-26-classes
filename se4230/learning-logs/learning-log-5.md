## Learning Log
- Question/Problem: What makes an algorithm 'greedy'?    
- When Identified: 9/9 6pm  
- Importance: 2. I don't think it's really needed, I just saw the term being used a few times  
- How to learn: Google/Youtube  
- Insight/Answer:  It's an adjective to describe an algorithm that chooses the best immediate option. Like, instant gratification algorithm. It will choose the right turn instead of a left turn, for example, even if it leads to a dead end just because it's immediately 'closer' to your destination than the left turn.  
- Hours Spent Learning: 1/4 
- Minutes Spent Documenting: 5 
- Confidence: 5   

- Question/Problem: How is it O(n) to sort an array of size n into the binary min heap ?    
- When Identified: 9/9 11am  
- Importance: 2. I get the gist but I'm just curious
- How to learn: Google/Youtube (found this gem: https://www.youtube.com/watch?v=8noP3YjjJCM) 
- Insight/Answer:  
    Given an unsorted array of size n:  
    - as a heap, n/2 nodes are in the bottom level and, consequently, leaf nodes (no children)  
    - supposedly, when you fix a node, all its descendants below are also fixed. This is because it BUBBLES down, not just switch with its immediate children!  
    - max tree height = log(n)  
    - something about these facts + simplifying the total # of swaps (sum of maximum swaps of one node per level, every node) with converging geometric sum...  
    - I don't get it once the mathematical deductions come up  
- Hours Spent Learning: 1 
- Minutes Spent Documenting: 5  
- Confidence: 2

- Question/Problem: Why shouldn't you use mutable objects as default values in Python arguments?  
- When Identified: 9/11 12am due to unexpected behavior of my Graph class...  
- Importance: 3. I mean, I could just NOT use it and go on with the assignment. I'm just curious why.  
- How to learn: Google... and some guy on Reddit asked this same question     
- Insight/Answer:    
  - Default args are evaluated only once at FUNCTION DEFINITION, not INVOKATION  
  - so, the mutable objects will be shared across calls  
  - that's stupid  
  - anyway, use ```None``` instead  
- Hours Spent Learning: 1/6 
- Minutes Spent Documenting: 5  
- Confidence: 5   

- Question/Problem: How am I supposed to make get_edges anything but O(n^2)?
- When Identified: 9/12 12am    
- Importance: 5. I kind of need to figure it out  
- How to learn: Google  
- Insight/Answer: Yield. That makes it a generator, which will produce the next item with the next() function. Calling list() and passing in the generator item as an argument will construct the list from the generator as normal.    
- Hours spent learning: 1/4  
- Minutes spent documenting: 5  
- Confidence: 5  