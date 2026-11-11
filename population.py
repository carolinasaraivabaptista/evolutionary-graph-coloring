"""A population maps unique identifiers to individuals."""
import coloring as col
import individual as ind


def new_population():
    return {"next_id": 0, "members": {}}


def add_individual(pop, individual):
    """Add an individual and return its new identifier."""
    identifier = pop["next_id"]
    pop["members"][identifier] = individual
    pop["next_id"] += 1
    return identifier


def get_individual(pop, identifier):
    """The individual with this identifier, or None if it has died."""
    return pop["members"].get(identifier)


def identifiers(pop):
    return list(pop["members"])


def size(pop):
    return len(pop["members"])


def kill(pop, identifier):
    pop["members"].pop(identifier, None)


def mutate_individual(pop, identifier, graph):
    """Try to improve the individual's colouring with one mutation."""
    individual = get_individual(pop, identifier)
    new_coloring = col.mutate(ind.get_coloring(individual), graph)
    pop["members"][identifier] = ind.new_individual(ind.get_birth(individual), new_coloring)


def reproduce_individual(pop, identifier, current_time, graph):
    """Add a mutated child of the individual. Returns the child's identifier."""
    parent = get_individual(pop, identifier)
    child_coloring = col.mutate(ind.get_coloring(parent), graph)
    return add_individual(pop, ind.new_individual(current_time, child_coloring))


def ranked(pop, graph):
    """Identifiers sorted from the best to the worst adapted."""
    return sorted(pop["members"],
                  key=lambda i: col.adaptation_degree(graph, ind.get_coloring(pop["members"][i])),
                  reverse=True)
