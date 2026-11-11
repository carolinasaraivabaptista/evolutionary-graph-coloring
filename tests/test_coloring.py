import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import coloring as col
import graph as gr
from simulator import simulate


def test_initial_coloring_is_valid():
    g = gr.petersen_graph()
    c = col.initial_coloring(g)
    assert col.num_colors(c) == 10
    assert col.count_defects(g, c) == 0


def test_defects_counted_once_per_edge():
    g = gr.add_edge(gr.new_graph(2), 0, 1)
    assert col.count_defects(g, {0: 0, 1: 0}) == 1


def test_mutation_never_makes_fitness_worse():
    g = gr.petersen_graph()
    c = col.initial_coloring(g)
    for _ in range(200):
        new = col.mutate(c, g)
        assert col.adaptation_degree(g, new) >= col.adaptation_degree(g, c)
        c = new


def test_simulation_returns_valid_coloring():
    import random
    random.seed(1)
    g = gr.petersen_graph()
    best = simulate(g, 50, 10, 1, 1, 25)
    assert best is not None
    assert col.count_defects(g, best) == 0
    assert col.num_colors(best) >= 3
