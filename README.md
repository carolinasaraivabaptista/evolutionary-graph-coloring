# Evolutionary Graph Colouring (Python)

A discrete-event **evolutionary simulation** that approximates the **chromatic number** of a graph: the smallest number of colours needed so that no two connected nodes share a colour. Finding it exactly is NP-hard, so a population of candidate colourings evolves until good solutions emerge.

Group project for *Elements of Programming* (Instituto Superior Técnico, 2023), refactored and documented in 2026.

## How it works

Every individual in the population is a colouring of the graph. It starts with one colour per node, which is valid but wasteful. Three kinds of events, scheduled at exponentially distributed random times in a priority queue, drive the evolution:

| Event | What happens |
|---|---|
| **Evaluation** | The individual may die. Death is more likely for poorly adapted and very young individuals. |
| **Evolution** | The individual either mutates (recolours one node with a colour already in use, kept only if fitness improves) or reproduces a mutated child. Reproduction is more likely when the population is small. |
| **Selection** | Invalid colourings are removed and the population is capped at 1.5 × its initial size. |

**Fitness:** a valid colouring scores `nodes / colours`, so fewer colours is better. An invalid one scores `1 / (1 + conflicts)`, which is always lower.

## Results

On the **Petersen graph** (10 nodes, 15 edges, chromatic number 3), with a population of 10 and a simulation time of 100:

| Colours found | Runs (out of 20) |
|:---:|:---:|
| 3 (optimal) | 15 |
| 4 | 5 |

Each run takes under a second.

## Running it

Requires Python 3.8+ and no external libraries.

```bash
python simulator.py                 # Petersen graph, default settings
python simulator.py --seed 1 --end-time 200 --population 20

pip install pytest && pytest        # run the tests
```

## Project structure

```
graph.py         # undirected graphs (dict of neighbour sets)
coloring.py      # colourings, conflicts, fitness and mutation
individual.py    # a colouring plus its birth time
population.py    # population with unique identifiers
event.py         # discrete events
event_queue.py   # pending-event queue sorted by time
exprandom.py     # exponential random times
simulator.py     # the simulation loop and command-line entry point
tests/           # pytest tests
```

The code follows an abstract-data-type style: each module exposes small functions that hide how the data is stored.

## Authors

Carolina Baptista and group colleagues, Instituto Superior Técnico.
