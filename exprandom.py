from math import log
from random import random


def exprandom(mean):
    """Exponentially distributed random time with the given mean."""
    return -mean * log(1 - random())
