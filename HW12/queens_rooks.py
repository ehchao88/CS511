from z3 import *
from random import sample
n: int = int(sys.argv[1])

p: int = math.ceil(n/3)

#generate random subset
queen_rows: [int] = sample(range(n), p)
    
#create z3 variables for board
queen_vars = ([[Bool('q'+str(i)+str(j)) for j in range(n)] for i in range(n)])
rook_vars = ([[Bool('r'+str(i)+str(j)) for j in range(n)] for i in range(n)])
s: Solver = Solver()

#phi_n,1
for row in queen_rows:
    s.add(Or([queen_vars[row][i] for i in range(n)]))

#phi_n,2
for i in range(n):
    if i not in queen_rows:
        s.add(Or([rook_vars[i][j] for j in range(n)]))

#phi_n,3
for i in range(n):
    for j in range(n):
        s.add(Implies(queen_vars[i][j], Not(rook_vars[i][j])))
    
#phi_n,4
for i in range(n):
    for j in range(n):
        not_taken = []
        for l in range(n):
            if l != j:
                not_taken.append(And(Not(queen_vars[i][l]), Not(rook_vars[i][l])))
        s.add(Implies(queen_vars[i][j], And(not_taken)))

#phi_n,5
for i in range(n):
    for j in range(n):
        not_taken = []
        for k in range(n):
            if k != i:
                not_taken.append(And(Not(queen_vars[k][j]), Not(rook_vars[k][j])))
        s.add(Implies(queen_vars[i][j], And(not_taken)))

#phi_n,6
for i in range(n):
    for j in range(n):
        not_taken = []
        for l in range(n):
            if l != j:
                not_taken.append(And(Not(queen_vars[i][l]), Not(rook_vars[i][l])))
        s.add(Implies(rook_vars[i][j], And(not_taken)))

#phi_n,7
for i in range(n):
    for j in range(n):
        not_taken = []
        for k in range(n):
            if k != i:
                not_taken.append(And(Not(queen_vars[k][j]), Not(rook_vars[k][j])))
        s.add(Implies(rook_vars[i][j], And(not_taken)))

#phi_n,8
for i in range(n):
    for j in range(n):
        not_taken = []
        for k in range(n):
            for l in range(n):
                if (k-l) == (i-j) and (k,l) != (i,j):
                    not_taken.append(And(Not(queen_vars[k][l]), Not(rook_vars[k][l])))
        s.add(Implies(queen_vars[i][j], And(not_taken))) 

#phi_n,9 
for i in range(n):
    for j in range(n):
        not_taken = []
        for k in range(n):
            for l in range(n):
                if (k+l) == (i+j) and (k,l) != (i,j):
                    not_taken.append(And(Not(queen_vars[k][l]), Not(rook_vars[k][l])))
        s.add(Implies(queen_vars[i][j], And(not_taken)))

if(s.check() == sat):
    m = s.model()
    queen_model = []
    rook_model = []
    for i in range(n):
        queen_row = []
        rook_row = []
        for j in range(n):
            queen_row.append(m[queen_vars[i][j]])
            rook_row.append(m[rook_vars[i][j]])
        queen_model.append(queen_row)
        rook_model.append(rook_row)
    print("queen_model")
    for row in queen_model:
        print(row)
    print("rook_model")
    for row in rook_model:
        print(row)