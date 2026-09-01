![Proof I can use images](./files/smiling-buck-tooth-emoji-smiling-buck-tooth-emoji-original.webp)  
<img src="./files/smiling-buck-tooth-emoji-smiling-buck-tooth-emoji-original.webp" alt="resized-proof" width="200" height="100">

## Learning Log  
- Question/Problem: Setting up Virtual Environments in Jupyter Notebook 
- When Identified: 8/30 1pm
- Importance (1-5): 2. Not really important, but I want to document certain things in Jupyter Notebook. 
- How to Learn: Review notes from Machine Learning class (this was where I learned about virtual environments & Jupyter Notebook)  
- Insight/Answer: A few steps, but it requires a requirements.txt file that the latter steps will use to install packages from, and then you link the kernel to the .ipynb file. I re-documented the steps I took and made it into its own file (inside a folder I keep as a tutorials reference).   
- Hours Spent Learning: 2/3
- Minutes Spent Documenting: 5 
- Confidence (1-5): 3.

- Question/Problem: Arrays & Hashing: solving interview-style questions
- When Identified: 8/30 12pm
- Importance (1-5): 3 
- How to Learn: Neetcode 150  
- Insight/Answer: I practiced my first ever question on Neetcode: Contains Duplicate. I ironically failed the first few tries trying to be clever by doing something about "sort the list. if the length - 1 + the first element is greater than the last element, there's a duplicate. [1 2 3 3] -> 4 - 1 + 1 = 4 > 3 TRUE: has duplicate." That case worked, but [100, 100, 200, 200, 300, 500, 600] -> 7 - 1 + 100 = 106 > 600 FALSE. No duplicate... false negative. That statement kind of would only work if the numbers consecutively touched. I solved it with bruteforce, only to realize that a Set would solve the logic in one line. Not hard to learn, but not sure how I could've missed that.
- Hours Spent Learning: 2/3
- Minutes Spent Documenting: 5 
- Confidence (1-5): 2

- Question/Problem: Pytests / Testing in Python. How can one file do both testing and the benchmark test? 
- When Identified: 8/31 11am
- Importance (1-5): 5. I need it to clarify for my assignment 
- How to Learn: ```I should be able to run python -m pytest sorting.py to run the tests and python sorting.py to run the benchmark.``` Um... so the same file can do different things with just different commands? wut   
Research how pytests work and go from there.
- Insight/Answer: Ok that was silly. I have done testing in Python before, just not enough to remember that pytests work by running the methods with test_ as the prefix of the name. There is also an auto-filled variable, _ _ name _ _ that can distinguish when the .py script is run from pytest vs. regularly, which is also how the benchmark will only run with ```python sorting.py```.  
- Hours Spent Learning: 0.5
- Minutes Spent Documenting: 10  
- Confidence (1-5): 4. The gaps remain in how I execute/write the code inside the testing and benchmark methods, but not why they work (which was the question here).  

- Question/Problem: Un-rust Big O Analysis Skills   
- When Identified: 8/31 11am
- Importance (1-5): 5. I need it for my assignment, which also did say I'll need to demonstrate the skill in exams.  
- How to Learn: Compile a list of the sorting methods I already know (have learnt, but possibly just need a refresh on what it is). Do best case and worst case and average case analyses.  
- Insight/Answer: I left out Quick Sort and Counting Sort, because I don't think I ever understood them deeply enough yet to begin with. I did Merge Sort, Insertion Sort, Selection Sort, and Bubble Sort since it's fresh in mind.  
- Hours Spent Learning: 2/3
- Minutes Spent Documenting: 10 
- Confidence (1-5): 3. I don't think I do super well with average cases.  

- Question/Problem: Learn Quick Sort and Counting Sort enough for the assignment     
- When Identified: 8/31 11am
- Importance (1-5): 5. I mean. I need it for the assignment
- How to Learn: Google and simulation websites, then go from there  
[ - Insight/Answer: I didn't spend time on this yet. Next learning log. Just documenting its founding ]   
[ - Hours Spent Learning: 0  ]
[ - Minutes Spent Documenting: 2  ] 
[ - Confidence (1-5): N/A ] 