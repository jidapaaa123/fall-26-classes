class PriorityQueue:

    def __init__(self):
        self.heap = []          # list of [priority, key]
        self.index_of = {}      # key -> index/location of the key inside self.heap 
        self.data_of = {}       # key -> data (just cuz the spec wants O(1))

    # ===_private_helpers===

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        # the key is in .heap[index]'s 2nd item
        self.index_of[self.heap[i][1]] = i
        self.index_of[self.heap[j][1]] = j

    def _sift_up(self, i):
        # i = current index viewed
        while i > 0:    
            parent = (i - 1) // 2
            if self.heap[i][0] < self.heap[parent][0]:
                self._swap(i, parent)
                i = parent
            else:
            # stop if already heavier than parent
                break

    def _sift_down(self, i):
        n = len(self.heap)
        # i = current index viewed
        while True:
            # get indices of 2 children
            left, right = 2 * i + 1, 2 * i + 2
            smallest = i
            
            # which of my kids is smaller than the current smallest
            if left < n and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < n and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right
            if smallest == i:
                break
            self._swap(i, smallest)
            i = smallest

    # ---------- public API ----------

    def update(self, key, priority, data=None, only_if_less=False):
        if key in self.index_of:
            i = self.index_of[key]
            old_priority = self.heap[i][0]
            if only_if_less and not (priority < old_priority):
                return  # new one is not less than current one
            self.heap[i][0] = priority
            self.data_of[key] = data
            
            if priority < old_priority:
                # might be even smaller?
                self._sift_up(i)
            else:
                self._sift_down(i)
        else:
            self.heap.append([priority, key])
            i = len(self.heap) - 1
            self.index_of[key] = i
            self.data_of[key] = data
            self._sift_up(i)

    def peek_min(self):
        return self.heap[0][1]

    def remove(self, key):
        i = self.index_of[key]
        last = len(self.heap) - 1
        self._swap(i, last)
        # easy to delete via .pop()
        self.heap.pop()
        del self.index_of[key]
        del self.data_of[key]
        
        if i < len(self.heap):  # only if we didn't just remove the last element
            # we don't know if the new thing that moved to i post-pop() is right
            #   for the spot
            self._sift_down(i)
            self._sift_up(i)

    def contains_key(self, key):
        return key in self.index_of

    def get_data(self, key):
        return self.data_of[key]

    def get_priority(self, key):
        return self.heap[self.index_of[key]][0]

    def count(self):
        return len(self.heap)
    

def test_new_priority_queue_has_count_zero():
    pq = PriorityQueue()
    assert pq.count() == 0

def test_update_adds_new_key():
    pq = PriorityQueue()
    pq.update("a", 5)
    assert pq.count() == 1
    assert pq.contains_key("a")

def test_peek_min_returns_smallest_priority_key():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.update("b", 2)
    pq.update("c", 9)
    assert pq.peek_min() == "b"

def test_peek_min_does_not_remove():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.peek_min()
    assert pq.count() == 1
    assert pq.contains_key("a")

def test_get_data_returns_associated_data():
    pq = PriorityQueue()
    pq.update("a", 5, data="hello")
    assert pq.get_data("a") == "hello"

def test_update_existing_key_changes_priority_without_duplicating():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.update("b", 1)
    pq.update("a", 0)  # "a" should now be the minimum
    assert pq.peek_min() == "a"
    assert pq.count() == 2  # still just two keys, not duplicated

def test_update_only_if_less_ignores_higher_priority():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.update("a", 10, only_if_less=True)  # 10 is not less than 5 -- should be ignored
    pq.update("b", 7)
    assert pq.peek_min() == "a"  # "a"'s priority should still be 5, which beats 7

def test_update_only_if_less_applies_lower_priority():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.update("b", 3)
    pq.update("a", 1, only_if_less=True)  # 1 is less than 5 -- should apply
    assert pq.peek_min() == "a"

def test_update_only_if_less_on_new_key_still_adds_it():
    pq = PriorityQueue()
    pq.update("a", 5, only_if_less=True)  # "a" wasn't present yet -- should still be added
    assert pq.contains_key("a")
    assert pq.count() == 1

def test_remove_deletes_key():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.update("b", 2)
    pq.remove("b")
    assert not pq.contains_key("b")
    assert pq.count() == 1
    assert pq.peek_min() == "a"

def test_remove_then_reinsert():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.remove("a")
    pq.update("a", 1)
    assert pq.contains_key("a")
    assert pq.peek_min() == "a"

def test_contains_key_false_for_absent_key():
    pq = PriorityQueue()
    assert not pq.contains_key("nonexistent")

def test_many_updates_and_removes_maintain_min_heap_order():
    pq = PriorityQueue()
    for key, priority in [("a", 5), ("b", 2), ("c", 8), ("d", 1), ("e", 9), ("f", 3)]:
        pq.update(key, priority)
    order = []
    while pq.count() > 0:
        m = pq.peek_min()
        order.append(m)
        pq.remove(m)
    assert order == ["d", "b", "f", "a", "c", "e"]

def test_get_priority_reflects_updated_priority():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.update("a", 2)  # same key, new priority
    assert pq.get_priority("a") == 2

def test_get_priority_unchanged_when_only_if_less_ignores_update():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.update("a", 10, only_if_less=True)  # should be ignored
    assert pq.get_priority("a") == 5

def test_get_priority_changed_when_only_if_less_applies():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.update("a", 1, only_if_less=True)  # should apply
    assert pq.get_priority("a") == 1