#! /usr/bin/env python
# -*- coding: utf-8 -*-

from vpqrsreducer import *

antisymmetric = True
G = G_complex
min_dim = 1
target_space = SPACE
model_space = SPACE

print('\n{:^80}\n'.format('COMPLEX CASE'))
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
print(basis)
# print(get_independent_basis(basis, G))
basis, dependent_elements = get_independent_basis(basis, G)
print(basis, dependent_elements)
print_transformation_table(basis, target_space, G)

