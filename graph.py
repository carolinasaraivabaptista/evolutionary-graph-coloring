"""Undirected graphs stored as a dict: node -> set of neighbours."""


def new_graph(num_nodes):
    """Empty graph with nodes 0 .. num_nodes-1.

    >>> new_graph(3)
    {0: set(), 1: set(), 2: set()}
    """
    return {node: set() for node in range(num_nodes)}


def add_edge(graph, node1, node2):
    """Add the edge node1 - node2 and return the graph."""
    graph.setdefault(node1, set()).add(node2)
    graph.setdefault(node2, set()).add(node1)
    return graph


def del_edge(graph, node1, node2):
    """Remove the edge node1 - node2 and return the graph."""
    graph.get(node1, set()).discard(node2)
    graph.get(node2, set()).discard(node1)
    return graph


def neighbours(graph, node):
    """Nodes connected to node."""
    return list(graph.get(node, set()))


def graph_dim(graph):
    """Number of nodes."""
    return len(graph)


def petersen_graph():
    """The Petersen graph (10 nodes, 15 edges, chromatic number 3)."""
    g = new_graph(10)
    edges = [(0, 1), (0, 4), (0, 5), (1, 2), (1, 6), (2, 3), (2, 7), (3, 4),
             (3, 8), (4, 9), (5, 7), (5, 8), (6, 8), (6, 9), (7, 9)]
    for a, b in edges:
        add_edge(g, a, b)
    return g
