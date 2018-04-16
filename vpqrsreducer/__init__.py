#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
>>> a = VerticalReflexion() % HorizontalReflexion()
>>> a.__mul__('abcd')
'dcba'
>>> a * 'vovo'
'ovov'
"""
import itertools
import sys


class BasisNotFound(Exception):
    pass


class GroupOperation(object):
    """
    >>> GroupOperation() * 'asdf'
    """
    mul_method = lambda self, string: None

    def __init__(self, name=""):
        self.name = name

    def is_identity(self):
        return False

    def __mod__(self, other):
        result = GroupOperation()
        result.name = self.name + '%' + other.name
        result.mul_method = lambda string: self * (other * string)
        return result

    def __mul__(self, string):
        return self.mul_method(string)

    def __repr__(self):
        return self.name or 'GroupOperation'


class Identity(GroupOperation):
    """
    >>> Identity() * 'asdf'
    'asdf'
    """
    mul_method = lambda self, string: string

    def is_identity(self):
        return True


class VerticalReflexion(GroupOperation):
    def __mul__(self, string):
        """
        >>> VerticalReflexion()*'vovo'
        'ovov'
        >>> VerticalReflexion()*'abcd'
        'badc'
        """
        middle = int(len(string)/2)
        middle_middle = int(middle/2)
        return string[0:middle][middle_middle:] \
            + string[0:middle][0:middle_middle] \
            + string[middle:][middle_middle:] \
            + string[middle:][0:middle_middle]


class VerticalReflexionTop(GroupOperation):
    def __mul__(self, string):
        """
        >>> VerticalReflexionTop() * 'abcd'
        'bacd'
        >>> HorizontalReflexion() % \
                VerticalReflexionTop() % HorizontalReflexion() * 'abcd'
        'abdc'
        """
        middle = int(len(string)/2)
        return string[0:middle][1] \
            + string[0:middle][0] \
            + string[middle:]


class HorizontalReflexion(GroupOperation):
    def __mul__(self, string):
        """
        >>> HorizontalReflexion()*'abcd'
        'cdab'
        >>> HorizontalReflexion()*'abcde'
        'cdeab'
        """
        middle = int(len(string)/2)
        return string[middle:] + string[0:middle]


class HorizontalReflexionLeft(GroupOperation):
    def __mul__(self, string):
        """
        >>> HorizontalReflexionLeft()*'abcd'
        'cbad'
        >>> HorizontalReflexionLeft()*'abcdef'
        'dbcaef'
        >>> HorizontalReflexionLeft()*'ab'
        'ba'
        """
        middle = int(len(string)/2)
        return string[middle:][0] + string[0:middle][1:] \
            + string[0:middle][0] + string[middle:][1:]


def get_orbit(string, group):
    return {g * string for g in group}


def spans_all(base, target_space, group):
    return target_space <= {g * b for g in group for b in base}


def get_representation(element, base, group):
    for g in group:
        for b in base:
            if element == g * b:
                return (g, b)


def string_to_particle_indices(string):
    """
    >>> string_to_particle_indices('vvvv')
    'abcd'
    >>> string_to_particle_indices('vovo')
    'aibj'
    """
    particles = 'abcdefgh'
    holes = 'ijklmno'
    result = ''
    p = 0
    h = 0
    for c in string:
        if c == 'v':
            result += particles[p]
            p += 1
        if c == 'o':
            result += holes[h]
            h += 1
    return result


def get_independent_basis(basis, G):
    """Discover dependencies in within the basis with the action G
    """
    new_basis = set()
    old_basis = set(basis)
    dependent_elements = set()
    for j in range(len(old_basis)):
        if len(old_basis) == 0:
            break
        b = old_basis.pop()
        for g in G:
            h = g * b
            if b == h:
                continue
            elif h in old_basis:
                old_basis.remove(h)
                dependent_elements.add(h)
        new_basis.add(b)
    return (new_basis, dependent_elements)


def find_generating_basis(
        target_space, model_space, G, min_dim=1, antisymmetric=False,
        antisymmetrizer=HorizontalReflexion('h') % VerticalReflexionTop('vt') %
        HorizontalReflexion('h')
        ):
    """Find a basis of string generating the target space through the G
    group
    :returns: Set with basis elements

    """
    print('G                 ', G)
    print('total_space  len: ', len(SPACE))
    print('target_space len: ', len(target_space))
    if antisymmetric:
        print('Expanding target space for antisimmetry')
        target_space = target_space \
            | {antisymmetrizer * c for c in target_space}
        print('target_space len: ', len(target_space))

    print('model_space  len: ', len(model_space))

    if len(model_space) == 0:
        print('Model space is too small')
        sys.exit(1)

    for dimension in range(min_dim, 2**len(model_space) + 1):
        print('Dimension: %s' % dimension)
        bases = [
            set(basis)
            for basis in itertools.combinations(model_space, dimension)
        ]
        if len(bases) == 0:
            print('I ran out of bases, your model space does not work')
            sys.exit(1)
        for basis in bases:
            if spans_all(set(basis), target_space, G):
                print('Base   ', basis)
                print('G*Base ', {g * b for g in G for b in basis})
                print('Target ', target_space)
                return basis
    raise BasisNotFound()


def print_transformation_table(basis, target_space, G):
    print()
    print('Transformation table:')
    for element in target_space:
        g, b = get_representation(element, basis, G)
        res = '%s = %s * %s' % (element, g, b)
        if b == element:
            continue
        print(res)


def get_inverse(g, G, basis):
    for h in G:
        is_inverse = True
        for c in basis:
            if not ((h % g * c) == c) and not ((g % h) * c == c):
                is_inverse = False
        if is_inverse:
            return h


e = Identity('e')
h = HorizontalReflexion('h')
v = VerticalReflexion('v')
hl = HorizontalReflexionLeft('hl')
vt = VerticalReflexionTop('vt')
vb = h % vt % h
vb.name = 'vb'
hr = v % hl % v
hr.name = 'hr'

G_complex = [e, h, v, h % v]
G_real = G_complex + [hl, hr]

SPACE = {"".join(d) for d in itertools.product('vo', repeat=4)}
