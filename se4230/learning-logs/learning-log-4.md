## Learning Log  
(- Question/Problem: How do I measure the benchmark of each algorithm?    
- When Identified: 9/2 5pm)  
- Importance: 5  
- How to Learn: I noticed retroactively that there IS sample code mentioned in the Project 1's details on this. So I went based off that  
- Insight/Answer: In order for it to compile, I just removed the parameter 'timeout' altogether. aggregated_time_sort() wanted to feed it to time_sort(), which does not take it. And turns out, in the 'main' loop, it just breaks the loop from increasing n if the time taken is more than the timeout threshold anyway. But the actual benchmarking parts make use of functions like time.perf_counter (performance counter) and statistics.median (find the median of the list of times). Everything else seemed basic, though it could be daunting if not used to Python's tool (or get past how MANY variables there are to set, especially if you want readable code). So it's literally just 'record the time for each algorithm, dealing with worst/best/average case, for varying sizes *n*. record the median. graph that info well." To that I am grateful for the sample code as it allows me to focus in on the heart of the assignment: Big O, instead of Python/graphing syntax  
- Hours Spent Learning: 1
- Minutes Spent Documenting: 5
- Confidence: 3.5. I sure can write pseudo code for it.

- Question/Problem: What is a priority queue (light review)  
- When Identified: 9/8 6pm  
- Importance: 4. Important but I don't expect the learning journey to be rough as I've already learned about it, but largely forgot    
- How to learn: Quick google search / the relevant section on Priority Queue in the linked PDF about Data Structures 
- Insight/Answer: Priority queue is an ADT that stores items with priorities that supports handling of 'finding/completing the highest priority item' essentially; arbitrary tie-breaking. Implementations could be as simple as a list, but the more recommended one is a binary min-heap 
- Hours spent learning: 1/6 
- Minutes spent documenting: 5 
- Confidence: 5  

- Question/Problem: What is a binary min heap  
- When Identified: 9/8 6pm   
- Importance: 5    
- How to learn: It turned out to be in the section right below the Priority Queue's  
- Insight/Answer: A tree in which smaller priorities are above larger priorities. Heap-ordering is such that parent index *i* have 2 children: *2i* and *2i + 1*. (Every child index *i* have its parent at *(i-1)//2*). This also implies that the minimum priority is at the top of the tree. 
- Hours spent learning: 1/4 
- Minutes spent documenting: 5 
- Confidence: 4  

- Question/Problem: What is Prim's algorithm? What does it do ?  
- When Identified: 9/8 6pm  
- Importance:    
- How to learn: The book talks about it + Youtube/Google
- Insight/Answer: The weight of a spanning tree is the sum of the weights of its edges. Prim's Algorithm is used to find Minimum Spanning Tree: a graph's spanning tree with minimum weight.  
  - similar to Dijkstra's algorithm for finding the shortest path
  - resulting MST cannot contain cycles  
  - algo: start at any node. Select the lowest-weight edge that connects to an UNVISITED node. Count that chosen node as visited, and repeat.  
  - **? So does this mean it can give different MST's from the same graph ?** --> apparently not (ignoring cases with ties)... there is a theorem/proof for this apparently
- Hours spent learning: 2/3 
- Minutes spent documenting: 10 
- Confidence: 3. I think this will improve after I complete the project 

==============================================================================================
(- Question/Problem: Un-rust Big O Analysis Skills Pt. 2  
- When Identified: 9/2 11am
- How to Learn: Emphasis on Quick Sort and Counting Sort. Review the sorting algorithms again: try to guess best/worst/average case scenario.)

(- Question/Problem: What are the 'siblings' of Big-O (concept)?  
- When Identified: 9/2 11am)

(- Question/Problem: How do I write sorting algorithms that require partitioning?  
- When Identified: 9/3 6pm)

(- Question/Problem: How do I convince myself Merge Sort is O(n*log(n))?  
- When Identified: 9/3 6pm)  


- Question/Problem: Understand difference between Big O vs. Omega vs. Theta in practice  
- When Identified: 9/4 11am  

- Question/Problem: How is it n to sort an array of size n into the binary min heap ?    
- When Identified: 9/9 11am  


- Question/Problem: How do I visually represent my graph (in Python)?  
- When Identified: 9/8 6pm  

- Question/Problem: What makes an algorithm 'greedy'?    
- When Identified: 9/9 6pm  

- Question/Problem: "... the minimum spanning tree and the shortest path tree are not the same" How come ?    
- When Identified: 9/9 6pm 