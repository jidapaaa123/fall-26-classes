# # example: "demo" -> "d", ("de", ("dem", None))
# def all_splits(s: str):
#     """Returns an immutable linked-list of word lists
#      'demo' ==> 'd', ('de', ('dem', None))"""
#     if len(s) < 2:
#         # list with just one list which has just the full string
#         # ex: "d" -> 
#         return ((s, ()), ())
    
#     splits_so_far = []
#     # how long is the first word?
#     for length_of_first_word in range(1, len(s)):
#         first_word = s[:length_of_first_word]
#         ways_to_split_rest = all_splits(s[length_of_first_word:])
#         for this_way in ways_to_split_rest:
#             splits_so_far = (first_word, (this_way)), splits_so_far

#     return splits_so_far

# example: "demo" -> "d", ("de", ("dem", None))
def all_splits(s: str):
    """Returns an immutable linked-list of word lists
     'demo' ==> 'd', ('de', ('dem', None))"""
    splits_so_far = ((s, ()), ())
    # how long is the first word?
    for length_of_first_word in range(1, len(s)):
        first_word = s[:length_of_first_word]
        ways_to_split_rest = all_splits(s[length_of_first_word:])
        for this_way in ways_to_split_rest:
            splits_so_far = (first_word, (this_way)), splits_so_far

    return splits_so_far

def tuples_to_list(cons_thing):
    a = []
    while cons_thing:
        first, cons_thing = cons_thing
        a.append(first)
    return a

def nested_tuples_to_list(cons_things):
    list_of_tuples = tuples_to_list(cons_things)
    return tuples_to_list(map(tuples_to_list, list_of_tuples))

print(all_splits("a")) # ( ('a', () ), ())
print(all_splits("ab"))
print(all_splits("demo"))
