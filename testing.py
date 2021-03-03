#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from sympy import Symbol, linsolve, linear_eq_to_matrix, solveset, FiniteSet, Eq, S, symbols, simplify, solve, And, satisfiable, Or

# generate symbols 
dim = 15
# this looks wrong but it actually is right 
tiles = np.array([[Symbol('cell_{}_{}'.format(j,i), integer=True) for i in range(dim)] for j in range(dim)])

knowledge_base = []
all_symbols = set()

# return the values for all symbols given according
# to our knowledge base
def get_symbols_in_kb(symbols: list) -> dict:
    ret = {}
    # symbols = [x if type(x) == Symbol else None for x in symbols]
    for sym in symbols:
        if sym in knowledge_base:
            ret[sym] = knowledge_base[sym]
    return ret

def add_to_knowledge_base(expr):
    symbols = expr.free_symbols
    for sym in symbols:
        # won't add duplicatese because its a set
        all_symbols.add(sym) 
    knowledge_base.append(expr)

# some expressions
add_to_knowledge_base(tiles[0,0])
add_to_knowledge_base(tiles[1,0]-1)
#add_to_knowledge_base(tiles[1,1])
add_to_knowledge_base(tiles[0,1] + tiles[1,0] + tiles[1,1] - 2)

print(tiles[1,0])

print(all_symbols)
A,b = linear_eq_to_matrix(knowledge_base, all_symbols)
print(A,b)

# use array of exprs
print(all_symbols)
t = linsolve((A,b), all_symbols)
print(t)
