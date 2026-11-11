"""An individual is a colouring together with its birth time."""


def new_individual(birth, coloring):
    return [birth, coloring]


def get_coloring(individual):
    return individual[1]


def get_birth(individual):
    return individual[0]


def get_age(individual, current_time):
    return current_time - individual[0]
