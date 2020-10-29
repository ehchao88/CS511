from z3 import *

#declare input and output variables
ina0, outa0, outa1, outa2, inb0, outb0 = Reals('ina0 outa0 outa1 outa2 ib0 outb0')

#establish phi_a to represent power3
phi_a = And(And(outa0 == ina0, outa1 == (outa0 * ina0)), (outa2 == (outa1 * ina0)))

#establish ph_b to represent power3_new
phi_b = (outb0 == (inb0 * inb0) * inb0)

#define wff psi
psi = Implies(And((ina0 == inb0), And(phi_a, phi_b)), (outa2 == outb0))

s: Solver = Solver()

#if not psi is not satisfiable, then psi is valid
s.add(Not(psi))
print(s.check())
