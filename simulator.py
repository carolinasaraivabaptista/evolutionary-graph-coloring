"""Discrete-event evolutionary simulation for the chromatic number problem.

Each individual is a colouring of the graph. Three kinds of events drive the
population:
  * evaluation - the individual may die; badly adapted and young ones die more often
  * evolution  - the individual mutates, or reproduces when the population is small
  * selection  - invalid colourings are removed and the population is capped
The answer is the best adapted colouring when the simulation ends.
"""
import argparse
import random
from math import atan, exp, pi

import coloring as col
import event as ev
import event_queue as eq
import graph as gr
import individual as ind
import population as popl
from exprandom import exprandom


def schedule_individual(queue, identifier, now, t_evaluation, t_evolution):
    queue = eq.add_event(queue, ev.new_event(now + exprandom(t_evaluation), "evaluation", identifier))
    queue = eq.add_event(queue, ev.new_event(now + exprandom(t_evolution), "evolution", identifier))
    return queue


def simulate(graph, end_time, k, t_evaluation, t_evolution, t_selection, history=None):
    """Run the simulation and return the best colouring found.

    graph        -- graph to colour
    end_time     -- simulation end time
    k            -- initial population size
    t_evaluation -- mean time between evaluations of an individual
    t_evolution  -- mean time between evolutions of an individual
    t_selection  -- mean time between selections
    history      -- optional list; (time, colours of the best valid colouring)
                    is appended every time the best colouring improves
    """
    queue = eq.new_queue()
    pop = popl.new_population()

    for _ in range(k):
        identifier = popl.add_individual(pop, ind.new_individual(0, col.initial_coloring(graph)))
        queue = schedule_individual(queue, identifier, 0, t_evaluation, t_evolution)
    queue = eq.add_event(queue, ev.new_event(t_selection, "selection", None))

    best = None
    while queue:
        current = eq.next_event(queue)
        queue = eq.remove_next(queue)
        now, kind, target = ev.time(current), ev.kind(current), ev.target(current)
        if now > end_time:
            break

        if kind == "selection":
            # Remove invalid colourings, then cap the population at 1.5 k
            for identifier in popl.identifiers(pop):
                if col.count_defects(graph, ind.get_coloring(popl.get_individual(pop, identifier))) != 0:
                    popl.kill(pop, identifier)
            for identifier in popl.ranked(pop, graph)[int(1.5 * k):]:
                popl.kill(pop, identifier)
            queue = eq.add_event(queue, ev.new_event(now + exprandom(t_selection), "selection", None))

        else:
            individual = popl.get_individual(pop, target)
            if individual is None:          # the individual has already died
                continue

            if kind == "evaluation":
                fitness = col.adaptation_degree(graph, ind.get_coloring(individual))
                age = ind.get_age(individual, now)
                p_death = 1 - (2 / pi) * atan((1 + fitness) ** (1 + 8 / (1 + age)))
                if random.random() < p_death:
                    popl.kill(pop, target)
                else:
                    queue = eq.add_event(queue, ev.new_event(now + exprandom(t_evaluation), "evaluation", target))

            elif kind == "evolution":
                p_mutation = 1 / (1 + exp((k - popl.size(pop)) / 10))
                if random.random() < p_mutation:
                    popl.mutate_individual(pop, target, graph)
                else:
                    child = popl.reproduce_individual(pop, target, now, graph)
                    queue = schedule_individual(queue, child, now, t_evaluation, t_evolution)
                queue = eq.add_event(queue, ev.new_event(now + exprandom(t_evolution), "evolution", target))

        # Remember the best valid colouring seen so far
        if popl.size(pop) > 0:
            top = ind.get_coloring(popl.get_individual(pop, popl.ranked(pop, graph)[0]))
            if col.count_defects(graph, top) == 0 and (best is None or col.num_colors(top) < col.num_colors(best)):
                best = top
                if history is not None:
                    history.append((now, col.num_colors(best)))

    return best


def main():
    parser = argparse.ArgumentParser(description="Approximate the chromatic number of the Petersen graph.")
    parser.add_argument("--end-time", type=float, default=100)
    parser.add_argument("--population", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    graph = gr.petersen_graph()
    best = simulate(graph, args.end_time, args.population, t_evaluation=1, t_evolution=1, t_selection=25)
    if best is None:
        print("No valid colouring survived. Try a longer run or another seed.")
        return
    print("Best colouring:", best)
    print("Colours used:", col.num_colors(best), "(chromatic number of the Petersen graph: 3)")


if __name__ == "__main__":
    main()
