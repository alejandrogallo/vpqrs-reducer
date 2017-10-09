from vpqrsreducer import *


def print_cc4s_code(basis, target_space, G):
    for element in target_space:
        g, b = get_representation(element, basis, G)
        if b == element:
            continue
        print_cc4s_tensor(element, b, basis, g, G)


def print_cc4s_tensor(element, base, basis, g, G):
    assert(base in basis)
    ginv = get_inverse(g, G, basis)
    # print('Inverse of %s = %s' % (g, ginv))
    element_tensor = 'V%s' % string_to_particle_indices(element)
    element_indices = string_to_particle_indices(element)
    base_tensor = 'V%s' % string_to_particle_indices(base)
    base_indices = ginv * element_indices
    print('if (%s) {' % element_tensor)
    print('  // %s = %s * %s' % (element, g, base))
    print('''\
  LOG(1, "CoulombIntegrals") << "Evaluating "
                             << %s->get_name() << " using "
                             << %s->get_name() << std::endl;
''' % (element_tensor, base_tensor) )
    print(
        '  (*{0})["{1}"] = (*{2})["{3}"];'.format(
            element_tensor,
            element_indices,
            base_tensor,
            base_indices
        )
    )
    print("  if (antisymmetrize) {")
    anti = vb * element
    anti_g, anti_b = get_representation(anti, basis, G)
    assert(anti_b in basis)
    anti_ginv = get_inverse(anti_g, G, basis)
    base_tensor = 'V%s' % string_to_particle_indices(anti_b)
    base_indices = anti_ginv % vb * string_to_particle_indices(element)
    print('    // %s = %s * %s' % (anti, anti_g, anti_b))
    print(
        '    (*{0})["{1}"] -= (*{2})["{3}"];'.format(
            element_tensor,
            element_indices,
            base_tensor,
            base_indices
        )
    )
    print("  }")
    print(
        '  allocatedTensorArgument("%sCoulombIntegrals", %s);' % (
            element.replace('v', 'P').replace('o', 'H'),
            element_tensor
        )
    )

    print("}")

#vim-run: make cc4s-real ; vi out/cc4s-real.cpp
