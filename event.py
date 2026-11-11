"""A discrete event: [time, kind, target identifier]."""


def new_event(time, kind, target):
    return [time, kind, target]


def time(e):
    return e[0]


def kind(e):
    return e[1]


def target(e):
    return e[2]
