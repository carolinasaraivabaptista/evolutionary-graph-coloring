"""Graph colourings stored as a dict: node -> colour (an int)."""
import random

import graph as gr


def initial_coloring(graph):
    """Random colouring where every node gets a different colour."""
    colors = list(range(gr.graph_dim(graph)))
    random.shuffle(colors)
    return {node: colors[node] for node in range(gr.graph_dim(graph))}


def color_list(coloring):
    """Colours used by the colouring."""
    return list(set(coloring.values()))


def num_colors(coloring):
    """Number of distinct colours used."""
    return len(set(coloring.values()))


def count_defects(graph, coloring):
    """Number of edges whose two ends have the same colour."""
    defects = sum(1 for node in graph for nb in graph[node]
                  if coloring[node] == coloring[nb])
    return defects // 2


def update_coloring(coloring, node, color):
    """Copy of the colouring with node recoloured."""
    new = coloring.copy()
    new[node] = color
    return new


def adaptation_degree(graph, coloring):
    """Fitness of a colouring.

    Valid colourings score nodes / colours (fewer colours is better).
    Invalid ones score 1 / (1 + defects), which is always lower.
    """
    defects = count_defects(graph, coloring)
    if defects == 0:
        return gr.graph_dim(graph) / num_colors(coloring)
    return 1 / (1 + defects)


def mutate(coloring, graph):
    """Recolour one random node with another colour already in use.

    The change is kept only if it improves the fitness.
    """
    node = random.choice(list(coloring))
    options = [c for c in color_list(coloring) if c != coloring[node]]
    if not options:
        return coloring
    candidate = update_coloring(coloring, node, random.choice(options))
    if adaptation_degree(graph, candidate) > adaptation_degree(graph, coloring):
        return candidate
    return coloring
