"""Pending event queue, kept sorted by time."""
import bisect

import event as ev


def new_queue():
    return []


def add_event(queue, e):
    times = [ev.time(x) for x in queue]
    queue.insert(bisect.bisect_right(times, ev.time(e)), e)
    return queue


def next_event(queue):
    if not queue:
        raise IndexError("the event queue is empty")
    return queue[0]


def remove_next(queue):
    if not queue:
        raise IndexError("the event queue is empty")
    return queue[1:]
