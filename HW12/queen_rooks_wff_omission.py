from z3 import *
from random import sample
n: int = int(sys.argv[1])

p: int = math.ceil(n/3)

#generate random subset
queen_rows: [int] = sample(range(n), p)
    
#create z3 variables for board
queen_vars = ([[Bool('q'+str(i)+str(j)) for j in range(n)] for i in range(n)])
rook_vars = ([[Bool('r'+str(i)+str(j)) for j in range(n)] for i in range(n)])

wffs = []
#phi_n,1
one = []
for row in queen_rows:
    one.append(Or([queen_vars[row][i] for i in range(n)]))
wffs.append(And([p for p in one]))
#phi_n,2
two = []
for i in range(n):
    if i not in queen_rows:
        two.append(Or([rook_vars[i][j] for j in range(n)]))
wffs.append(And([p for p in two]))
#phi_n,3
three = []
for i in range(n):
    for j in range(n):
        three.append(Implies(queen_vars[i][j], Not(rook_vars[i][j])))
wffs.append(And([p for p in three]))  
#phi_n,4
four = []
for i in range(n):
    for j in range(n):
        not_taken = []
        for l in range(n):
            if l != j:
                not_taken.append(And(Not(queen_vars[i][l]), Not(rook_vars[i][l])))
        four.append(Implies(queen_vars[i][j], And(not_taken)))
wffs.append(And([p for p in four]))
#phi_n,5
five = []
for i in range(n):
    for j in range(n):
        not_taken = []
        for k in range(n):
            if k != i:
                not_taken.append(And(Not(queen_vars[k][j]), Not(rook_vars[k][j])))
        five.append(Implies(queen_vars[i][j], And(not_taken)))
wffs.append(And([p for p in five]))
#phi_n,6
six = []
for i in range(n):
    for j in range(n):
        not_taken = []
        for l in range(n):
            if l != j:
                not_taken.append(And(Not(queen_vars[i][l]), Not(rook_vars[i][l])))
        six.append(Implies(rook_vars[i][j], And(not_taken)))
wffs.append(And([p for p in six]))
#phi_n,7
seven = []
for i in range(n):
    for j in range(n):
        not_taken = []
        for k in range(n):
            if k != i:
                not_taken.append(And(Not(queen_vars[k][j]), Not(rook_vars[k][j])))
        seven.append(Implies(rook_vars[i][j], And(not_taken)))
wffs.append(And([p for p in seven]))
#phi_n,8
eight = []
for i in range(n):
    for j in range(n):
        not_taken = []
        for k in range(n):
            for l in range(n):
                if (k-l) == (i-j) and (k,l) != (i,j):
                    not_taken.append(And(Not(queen_vars[k][l]), Not(rook_vars[k][l])))
        eight.append(Implies(queen_vars[i][j], And(not_taken))) 
wffs.append(And([p for p in eight]))
#phi_n,9
nine = [] 
for i in range(n):
    for j in range(n):
        not_taken = []
        for k in range(n):
            for l in range(n):
                if (k+l) == (i+j) and (k,l) != (i,j):
                    not_taken.append(And(Not(queen_vars[k][l]), Not(rook_vars[k][l])))
        nine.append(Implies(queen_vars[i][j], And(not_taken)))
wffs.append(And([p for p in nine]))
omitted_wffs = []
for i in range(len(wffs)):
    keep_wffs = []
    for j in range(len(wffs)):
        if i != j:
            keep_wffs.append(wffs[j])
    s:Solver = Solver()
    for kw in keep_wffs:
        s.add(kw)
    s.add(Not(wffs[i]))
    if(s.check() == unsat):
        omitted_wffs.append(i)

print(omitted_wffs)
#if(s.check() == sat):
#    m = s.model()
#    queen_model = []
#    rook_model = []
#    for i in range(n):
#        queen_row = []
#        rook_row = []
#        for j in range(n):
#            queen_row.append(m[queen_vars[i][j]])
#            rook_row.append(m[rook_vars[i][j]])
#        queen_model.append(queen_row)
#        rook_model.append(rook_row)
#    print("queen_model")
#    for row in queen_model:
#        print(row)
#    print("rook_model")
#    for row in rook_model:
#        print(row)