from z3 import *

x, y, v = 12, 15, 6
w = Int('w')

phi = ForAll(w, ((And((x%w == 0), (y%w == 0)) == (v%w == 0))))

s: Solver = Solver()
s.add(phi)
print(s.check())