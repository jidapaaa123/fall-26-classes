## Learning Log  
(- Question/Problem: Un-rust Big O Analysis Skills Pt. 2  
- When Identified: 9/2 11am
- How to Learn: Emphasis on Quick Sort and Counting Sort. Review the sorting algorithms again: try to guess best/worst/average case scenario.)

(- Question/Problem: What are the 'siblings' of Big-O (concept)?  
- When Identified: 9/2 11am)

(- Question/Problem: How do I measure the benchmark of each algorithm?    
- When Identified: 9/2 5pm)  
- Importance: 5  
- How to Learn: I noticed retroactively that there IS sample code mentioned in the Project 1's details on this. So I went based off that  
- Insight/Answer: In order for it to compile, I just removed the parameter 'timeout' altogether. aggregated_time_sort() wanted to feed it to time_sort(), which does not take it. And turns out, in the 'main' loop, it just breaks the loop from increasing n if the time taken is more than the timeout threshold anyway. But the actual benchmarking parts make use of functions like time.perf_counter (performance counter) and statistics.median (find the median of the list of times). Everything else seemed basic, though it could be daunting if not used to Python's tool (or get past how MANY variables there are to set, especially if you want readable code). So it's literally just 'record the time for each algorithm, dealing with worst/best/average case, for varying sizes *n*. record the median. graph that info well." To that I am grateful for the sample code as it allows me to focus in on the heart of the assignment: Big O, instead of Python/graphing syntax  
- Hours Spent Learning: 1
- Minutes Spent Documenting: 5
- Confidence: 3.5. I sure can write pseudo code for it.

(- Question/Problem: How do I write sorting algorithms that require partitioning?  
- When Identified: 9/3 6pm)

(- Question/Problem: How do I convince myself Merge Sort is O(n*log(n))?  
- When Identified: 9/3 6pm)  


- Question/Problem: Understand difference between Big O vs. Omega vs. Theta in practice  
- When Identified: 9/4 11am  