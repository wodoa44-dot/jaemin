from functools import partial
import logging

class Infix(object):
    def __init__(self, func):
        self.func = func

    def __or__(self, other):
        return self.func(other)

    def __ror__(self, other):
        return Infix(partial(self.func, other))

    def __call__(self, v1, v2):
        return self.func(v1, v2)

@Infix
def implies(p, q):
    return not p or q

@Infix
def iff(p, q):
    return (p |implies| q) and (q |implies| p) 

@Infix
def xor(p, q):
    return (not p and q) or (p and not q) 

@Infix
def eq(p, q):
    return not (p |xor| q)


