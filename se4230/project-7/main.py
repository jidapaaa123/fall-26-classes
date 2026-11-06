from graph import Graph


def reverse_graph(G):
    reversed_G = Graph()

    for node in G.get_nodes():
        reversed_G.add_node(node, G.get_node_data(node))

    # edges are reversed
    for parent, child in G.get_edges():
        reversed_G.add_edge(child, parent, G.get_edge_data(parent, child))

    return reversed_G




def dfs_finish_order(G):
    visited = set()
    order = []

    def visit(node):
        visited.add(node)
        for child in G.get_children(node):
            if child not in visited:
                visit(child)
        order.append(node)

    for root in G.get_nodes():
        if root not in visited:
            visit(root)

    return order

def kosaraju_meta_graph(G):
    order = dfs_finish_order(G)
    R = reverse_graph(G)

    # each DFS tree is one SCC
    visited = set()
    component_of = {}   # SCC of node [x]
    components = []     # frozenset ; SCC 

    def collect(node, members):
        visited.add(node)
        members.add(node)
        for child in R.get_children(node):
            if child not in visited:
                collect(child, members)

    # DFS on the reversed graph, in reverse finish order "decreasing finish time"
    for root in reversed(order):
        if root not in visited:
            members = set()
            collect(root, members)
            scc = frozenset(members)
            components.append(scc)
            for n in members:
                component_of[n] = scc

    # meta graph
    meta = Graph()
    for scc in components:
        meta.add_node(scc)

    for u, v in G.get_edges():
        cu, cv = component_of[u], component_of[v]
        if cu != cv:                  # skip edges inside an SCC
            meta.add_edge(cu, cv)     

    return meta