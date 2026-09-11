# QUESTION: so the main part of the project is  
# to test to show that our ADT implementations are
# compatible with the Prim's alg (we're not modifying Prim's alg?)

# QUESTION: Why does Graph need a data in the constructor?
#   if we're storing both nodes' and edges' data...
#   then do we have 'nodes_data' and 'edges_data' as fields
#   instead of just 'data'?

class Graph:
    nodes: dict
    nodes_data: dict
    edges: dict
    
    def __init__(self, nodes=None, nodes_data={}, edges=None,):
        self.nodes = nodes if nodes is not None else {} 
        self.nodes_data = nodes_data if nodes_data is not None else {}
        self.edges = edges if edges is not None else {}
        
    
    def add_node(self, node, data=None):
        if node in self.nodes:
            return
        self.nodes[node] = {}
        self.nodes_data[node] = data
        
    def add_edge(self, parent, child, data=None):
        """Assumes parent and child are already 
        present as nodes (via add_node) -- 
        this method does not create nodes 
        automatically."""
        
        print(self.nodes)
        print(self.edges)
        
        # skip if reverse direction exists
        if child in self.edges and parent in self.edges[child]:
            return
        
        self.edges[parent] = {}
        self.edges[parent][child] = {data}
    
    def get_node_data(self, node):
        if node not in self.nodes:
            raise ValueError(f"Node {node} not in graph")
        
        print(f"From get_node_data")
        print(f"Nodes: {self.nodes}")
        print(f"Data: {self.nodes_data}")
        return self.nodes_data[node]
        
    def contains_node(self, node):
        return node in self.nodes
    
    def contains_edge(self, parent, child):
        return child in self.edges[parent]
    
    def get_nodes(self):
        return self.nodes.copy()
    
        
    
    
        
        

    
    
    
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