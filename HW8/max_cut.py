from z3 import *
import sys
import ast

#taking input and converting to objective function and constraints
p = open(sys.argv[1], 'r')
p_lines = p.readlines()
weights = p_lines[0].strip('\n').strip('w = ')
weights = ast.literal_eval(weights)
g = ""
p_lines[1] = p_lines[1].strip('\n').strip('c = ')
g += p_lines[1]
for line in p_lines[2:]:
    g += line.strip('\n')
graph = ast.literal_eval(g)

#create z3 variables for characteristic vector
vars = ([Int('x'+str(i+1)) for i in range(len(weights))])
#print(vars)



def max_cut(gt):
    s: Solver = Solver()
    #Make sure the characteristic vector contains only 1s and 0s
    for var in vars:
        s.add(Or(var == 0, var == 1))

    #find the capacity of the cut using the pb-function (5)
    cap = 0
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if i != j:
                cap += graph[i][j] * ((vars[i]*(1-vars[j]))+((1-vars[i])*vars[j]))

    #get rid of double counts of edges
    cap /= 2
    #add constraint that the capacity must be greater than the inputted minimum
    s.add(cap > gt)

    if s.check() == sat:
        #if it is satisfiable, model and find the capacity based on that model
        m = s.model()
        cur_cap = 0
        for i in range(len(graph)):
            for j in range(len(graph[i])):
                cur_cap += graph[i][j] * ((m[vars[i]].as_long()*(1-m[vars[j]].as_long()))+((1-m[vars[i]].as_long())*m[vars[j]].as_long()))
        cur_cap /= 2
        #recursively call the function, with this capacity as the new floor
        new_max = max_cut(cur_cap)

        #if you can't create a cut with a greater capacity, then this is max-cut, so return the model along with the capacity
        if new_max == False:
            mod = []
            for i in range(len(vars)):
                mod.append(m[vars[i]])
            return [mod, cur_cap]
        #otherwise return the greater max cut
        else:
            return new_max
    #if unsat, return false
    else:
        return False

max_c = max_cut(0)
if max_c == False:
    print("Max cut not found")

else:
    print("Max cut found\nCharacteristic vector:", max_c[0], "\nMax_cut capacity:", max_c[1])