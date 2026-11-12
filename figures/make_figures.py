"""Generate the README figures. Requires matplotlib (pip install matplotlib).

    python figures/make_figures.py
"""
import os
import random
import sys
from math import cos, pi, sin

import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import coloring as col  # noqa: E402
import graph as gr  # noqa: E402
from simulator import simulate  # noqa: E402

INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a"]  # three validated categorical slots
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "text.color": INK,
                     "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})


def petersen_positions():
    """Outer pentagon (nodes 0-4) and inner pentagram (nodes 5-9)."""
    pos = {}
    for i in range(5):
        a = pi / 2 - 2 * pi * i / 5
        pos[i] = (cos(a), sin(a))
        pos[i + 5] = (0.5 * cos(a), 0.5 * sin(a))
    return pos


def draw_coloring(ax, graph, coloring, palette, title):
    pos = petersen_positions()
    for node in graph:
        for nb in graph[node]:
            if node < nb:
                (x1, y1), (x2, y2) = pos[node], pos[nb]
                ax.plot([x1, x2], [y1, y2], color="#b9b8b2", lw=2, zorder=1)
    for node, (x, y) in pos.items():
        ax.scatter(x, y, s=520, color=palette[coloring[node]], edgecolor="white",
                   linewidth=2.5, zorder=2)
    ax.set_title(title, color=INK, fontsize=13, pad=10)
    ax.set_aspect("equal")
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.15, 1.25)
    ax.axis("off")


def hero(graph):
    """Petersen graph: initial colouring (10 colours) next to the best one found."""
    random.seed(3)
    start = col.initial_coloring(graph)
    best = simulate(graph, 100, 10, 1, 1, 25)
    assert col.num_colors(best) == 3 and col.count_defects(graph, best) == 0

    # 10 distinct colours for the starting point: a soft spectrum is fine here,
    # the point is only "every node is different"
    cmap = plt.get_cmap("tab10")
    start_palette = {c: cmap(c) for c in range(10)}
    best_palette = {c: SERIES[i] for i, c in enumerate(sorted(set(best.values())))}

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), facecolor="white")
    draw_coloring(axes[0], graph, start, start_palette, "Start: 10 colours (one per node)")
    draw_coloring(axes[1], graph, best, best_palette, "After evolution: 3 colours (optimal)")
    fig.text(0.5, 0.5, "→", ha="center", va="center", fontsize=40, color=MUTED)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "petersen_coloring.png"), dpi=150, facecolor="white")
    plt.close(fig)


def convergence(graph, runs=20):
    """Colours used by the best valid colouring over time, one line per run."""
    fig, ax = plt.subplots(figsize=(9, 4.2), facecolor="white")
    finals = []
    for seed in range(runs):
        random.seed(seed)
        history = []
        simulate(graph, 100, 10, 1, 1, 25, history=history)
        times = [0] + [t for t, _ in history] + [100]
        colours = [10] + [c for _, c in history] + [history[-1][1]]
        finals.append(colours[-1])
        color = SERIES[0] if colours[-1] == 3 else SERIES[1]
        ax.step(times, colours, where="post", color=color, lw=2, alpha=0.55)
    ax.axhline(3, color=MUTED, lw=1, ls="--")
    ax.text(100, 3.15, "chromatic number = 3", ha="right", va="bottom", color=MUTED, fontsize=10)
    ax.set_xlabel("Simulation time")
    ax.set_ylabel("Colours in best valid colouring")
    ax.set_xlim(0, 100)
    ax.set_ylim(2, 10.5)
    ax.set_yticks(range(2, 11))
    ax.grid(axis="y", color=GRID, lw=1)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0)
    n3 = finals.count(3)
    ax.plot([], [], color=SERIES[0], lw=2, label=f"ended at 3 colours ({n3} runs)")
    ax.plot([], [], color=SERIES[1], lw=2, label=f"ended at 4+ colours ({runs - n3} runs)")
    ax.legend(frameon=False, loc="upper right")
    ax.set_title(f"{runs} independent runs on the Petersen graph", color=INK, loc="left", fontsize=13)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "convergence.png"), dpi=150, facecolor="white")
    plt.close(fig)
    return finals


if __name__ == "__main__":
    g = gr.petersen_graph()
    hero(g)
    finals = convergence(g)
    print("Final colour counts over 20 runs:", sorted(finals))
