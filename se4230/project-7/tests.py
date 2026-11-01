from graph import Graph
from main import reverse_graph, dfs_finish_order, kosaraju_meta_graph

# ==========================PART 1: reverse_graph==========================
def build(nodes, edges):
    g = Graph()
    for n in nodes:
        g.add_node(n)
    for e in edges:
        g.add_edge(*e)
    return g

def test_reverse_preserves_node_and_edge_data():
    g = Graph()
    g.add_node("a", data="A")
    g.add_node("b", data="B")
    g.add_edge("a", "b", data=42)
    r = reverse_graph(g)
    assert r.get_node_data("a") == "A"
    assert r.get_node_data("b") == "B"
    assert r.get_edge_data("b", "a") == 42

def test_reverse_does_not_modify_original():
    g = build(["a", "b"], [("a", "b")])
    reverse_graph(g)
    assert g.contains_edge("a", "b")
    assert not g.contains_edge("b", "a")

def test_reverse_parents_and_children_swap():
    g = build(["a", "b", "c"], [("a", "b"), ("a", "c")])
    r = reverse_graph(g)
    assert set(r.get_parents("a")) == {"b", "c"}
    assert set(r.get_children("b")) == {"a"}

# ==========================PART 2: dfs_finish_order==========================
def test_finish_order_chain():
    g = build(["a", "b", "c"], [("a", "b"), ("b", "c")])
    assert dfs_finish_order(g) == ["c", "b", "a"]

def test_finish_order_cycle():
    g = build(["a", "b", "c"], [("a", "b"), ("b", "c"), ("c", "a")])
    assert dfs_finish_order(g) == ["c", "b", "a"]

def test_finish_order_disconnected_components():
    g = build(["a", "b", "c", "d"], [("a", "b"), ("c", "d")])
    assert dfs_finish_order(g) == ["b", "a", "d", "c"]

def test_finish_order_root_of_a_dfs_tree_finishes_last_in_its_tree():
    g = build(["a", "b", "c"], [("a", "b"), ("a", "c")])
    assert dfs_finish_order(g)[-1] == "a"

# ==========================PART 3: kosaraju_meta_graph==========================
def make_example_graph():
    """cycle 0,1,2 -> 3 -> cycle 4,5,6 -> 7 (diagonal is 6->4)."""
    g = Graph()
    for i in range(8):
        g.add_node(i)

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 6)
    g.add_edge(6, 4)
    g.add_edge(4, 7)
    g.add_edge(6, 7)
    return g

def test_example_sccs_are_correct():
    meta = kosaraju_meta_graph(make_example_graph())
    assert set(meta.get_nodes()) == {
        frozenset({0, 1, 2}),
        frozenset({3}),
        frozenset({4, 5, 6}),
        frozenset({7}),
    }

def test_example_nodes_are_in_topological_order():
    meta = kosaraju_meta_graph(make_example_graph())

    position = {}
    index = 0
    for node in meta.get_nodes():
        position[node] = index
        index = index + 1

    for parent, child in meta.get_edges():
        assert position[parent] < position[child]