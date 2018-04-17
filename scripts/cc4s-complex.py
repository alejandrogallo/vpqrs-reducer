#! /usr/bin/env python
# -*- coding: utf-8 -*-

from vpqrsreducer import *
from cc4s import *

antisymmetric = True
G = G_complex
min_dim = 6
target_space = SPACE
model_space = SPACE

print('\n{:^80}\n'.format('COMPLEX CASE'))
basis = find_generating_basis(
    target_space, model_space, G, min_dim=min_dim,
    antisymmetric=antisymmetric, antisymmetrizer=vb
)

# print_transformation_table(basis, target_space, G)

# This basis is not the smallest
basis = {
    'vvoo',
    'oovv',
    'voov',
    'vovo',
    'oooo',
    'ooov',
    'vooo',
    'vvvv',
    'vovv',
}
print('Fixed  basis:', basis)
print('Basis length:', len(basis))
cleaned_basis, dependent_elements = get_independent_basis(basis, G)
print("2 dependent elements in basis:")
print(dependent_elements)

target_space = SPACE - basis
print('Target space:')
print(target_space)
print('Target space length:', len(target_space))

print_transformation_table(basis, target_space, G)
print()

print_tensor_definitions(target_space, complex_version=True)
print_cc4s_code(
    basis, target_space, G, complex_version=True
)

#vim-run: make cc4s-complex ; vi +'set ft=cpp' out/cc4s-complex.out
#vim-run: make cc4s-complex
#vim-run: make cc4s-complex ; vi out/cc4s-complex.cpp
