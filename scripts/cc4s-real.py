#! /usr/bin/env python
# -*- coding: utf-8 -*-

from vpqrsreducer import *
from cc4s import *

antisymmetric = True
G = G_real
min_dim = 6
target_space = SPACE
model_space = SPACE

print('\n{:^80}\n'.format('REAL CASE'))
basis = find_generating_basis(
    target_space, model_space, G, min_dim=min_dim,
    antisymmetric=antisymmetric, antisymmetrizer=vb
)

# print_transformation_table(basis, target_space, G)

basis = {
    'vovo',
    'vvoo',
    'oovv',
    'voov',
    'oooo',
    'ooov',
    'vooo',
    'vvvv',
    'vvvo'
}
print('Initial basis: %s' % basis)
basis, dependent_elements = get_independent_basis(basis, G)
print('Cleaned basis: %s, %s' %(basis, dependent_elements))
print_transformation_table(basis, target_space, G)
print_cc4s_code(basis, target_space, G)

#vim-run: make cc4s-real
