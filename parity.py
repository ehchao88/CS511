from z3 import *

#declaring boolean variables
p1, p2, p3, p4 = Bools ('p1 p2 p3 p4')

#define conjunctive normal form phi
phi = And(Or(p1, Not(p2), Not(p3), Not(p4)), Or(Not(p1), p2, Not(p3), Not(p4)), Or(Not(p1), Not(p2), p3, (Not(p4))), Or(Not(p1), Not(p2), Not(p3), p4),
            Or(Not(p1), p2, p3, p4), Or(p1, Not(p2), p3, p4), Or(p1, p2, Not(p3), p4), Or(p1, p2, p3, Not(p4)))

#define disjunctive normal form psi
psi = Or(And(p1, p2, Not(p3), Not(p4)), And(p1, p3, Not(p2), Not(p4)), And(p1, p4, Not(p2), Not(p3)), And(p2, p3, Not(p1), Not(p4)), And (p2, p4, Not(p1), Not(p3)),
            And(p3, p4, Not(p1), Not(p2)), And(p1, p2, p3, p4), And(Not(p1), Not(p2), Not(p3), Not(p4)))

#define biconditional only function theta
theta = Not(Not(p1 == p2 == p3 == p4))

s: Solver = Solver()
s.add(phi != psi)
s.add(phi != theta)
s.add(psi != theta)
print(s.check())