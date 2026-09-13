class Graph:
    nodes: dict
    children: dict
    parents: dict
    
    def __init__(self, nodes=None, children=None, parents=None):
        self.nodes = nodes if nodes is not None else {} 
        self.children = children if children is not None else {}
        self.parents = parents if parents is not None else {}
    
    def add_node(self, node, data=None):
        if node in self.nodes:
            return
        self.nodes[node] = data
        
    def add_edge(self, parent, child, data=None):
        """Assumes parent and child are already 
        present as nodes (via add_node) -- 
        this method does not create nodes 
        automatically."""
        
        if parent not in self.children.keys():
            # first kid!
            self.children[parent] = {}
        self.children[parent][child] = data
        
        if child not in self.parents.keys():
            # first papa!
            self.parents[child] = {}
        self.parents[child][parent] = data
    
    def add_undirected_edge(self, node1, node2, data=None):
        self.add_edge(node1, node2, data)
        self.add_edge(node2, node1, data)
    
    def get_node_data(self, node):
        if node not in self.nodes:
            raise ValueError(f"Node {node} not in graph")
        return self.nodes[node]
    
    def get_edge_data(self, parent, child):
        return self.children[parent][child]
    
    def get_children(self, parent):
        return self.children.get(parent, {}).keys()
    
    def get_parents(self, node):
        return self.parents.get(node, {}).keys()

    def contains_node(self, node):
        return node in self.nodes
    
    def contains_edge(self, parent, child):
        if parent not in self.children.keys():
            return False
        return child in self.children[parent]
    
    def get_nodes(self):
        return self.nodes.keys()
    
    def get_edges(self):
        for key, val in self.children.items():
            for v in val:
                yield (key, v)
    
def test_new_graph_has_no_nodes():
    graph = Graph()
    assert list(graph.get_nodes()) == []

def test_add_node_then_contains_node():
    graph = Graph()
    graph.add_node("a")
    assert graph.contains_node("a")
    assert not graph.contains_node("b")

def test_add_node_is_idempotent():
    graph = Graph()
    graph.add_node("a", data=1)
    graph.add_node("a", data=2)  # already present -- should not duplicate
    assert list(graph.get_nodes()) == ["a"]

def test_get_node_data():
    graph = Graph()
    graph.add_node("a", data="hello")
    assert graph.get_node_data("a") == "hello"

def test_add_edge_then_contains_edge():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_edge("a", "b", data=5)
    assert graph.contains_edge("a", "b")
    assert not graph.contains_edge("b", "a")  # directed, so the reverse shouldn't exist

def test_get_edge_data():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_edge("a", "b", data=5)
    assert graph.get_edge_data("a", "b") == 5

def test_add_undirected_edge_creates_both_directions():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_undirected_edge("a", "b", data=7)
    assert graph.contains_edge("a", "b")
    assert graph.contains_edge("b", "a")
    assert graph.get_edge_data("a", "b") == 7
    assert graph.get_edge_data("b", "a") == 7

def test_get_children():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_node("c")
    graph.add_edge("a", "b")
    graph.add_edge("a", "c")
    assert set(graph.get_children("a")) == {"b", "c"}

def test_get_nodes_preserves_insertion_order():
    graph = Graph()
    graph.add_node("c")
    graph.add_node("a")
    graph.add_node("b")
    assert list(graph.get_nodes()) == ["c", "a", "b"]

def test_get_edges_preserves_insertion_order():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_node("c")
    graph.add_edge("a", "b")
    graph.add_edge("a", "c")
    assert list(graph.get_edges()) == [("a", "b"), ("a", "c")]

def test_contains_node_false_for_absent_node():
    graph = Graph()
    assert not graph.contains_node("nonexistent")

def test_contains_edge_false_for_absent_edge():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    assert not graph.contains_edge("a", "b")
    
# why was this not here?
def test_get_parents():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_edge("a", "b")
    assert set(graph.get_parents("b")) == {"a"}
    
# ========= PRIORITY QUEUE ========
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

# ========= PRIM'S ALGORITHM ========
def prim_mst(graph, edge_weight=None, start_node=None):
    """
    Find minimum spanning tree using Prim's algorithm.
    
    Args:
        graph: an instance of your Graph data structure
        start_node: the node to start from; if None, uses first node from graph.get_nodes()
        edge_weight: function taking (parent, child) returning edge weight;
                     if None, uses edge data as weight
    
    Returns:
        Graph instance containing the minimum spanning tree
    """
    if edge_weight is None:
        edge_weight = lambda parent, child: graph.get_edge_data(parent, child)
    
    if start_node is None:
        start_node = next(iter(graph.get_nodes()))
    
    mst = Graph()  # assuming your Graph class is named Graph
    pq = PriorityQueue()  # assuming your PriorityQueue class is named PriorityQueue
    
    pq.update(start_node, 0, data=None)
    
    while pq.count() > 0:
        current_node = pq.peek_min()
        parent_node = pq.get_data(current_node)
        pq.remove(current_node)
        
        if not mst.contains_node(current_node):
            mst.add_node(current_node)
            if parent_node is not None:
                data = graph.get_edge_data(parent_node, current_node)
                mst.add_undirected_edge(parent_node, current_node, data=data)
            
            for child in graph.get_children(current_node):
                if not mst.contains_node(child):
                    weight = edge_weight(current_node, child)
                    pq.update(child, weight, data=current_node, only_if_less=True)
    
    return mst