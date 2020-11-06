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

def max_weight(gt):
    s: Solver = Solver()
    #Make sure characteristic vector contains only 1s and 0s
    for var in vars:
        s.add(Or(var == 0, var == 1))
    
    #Summate over the weights of all nodes in the subset
    sub_weight = 0
    for i in range(len(vars)):
        sub_weight += weights[i]*vars[i]
    
    #find max weight and add 1
    max_w_plus_1 = 1+max(weights)

    #find capacities of the edges in the subset
    cap = 0
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if i != j:
                cap += graph[i][j] * vars[i] * vars[j]
    #get rid of double edge counts
    cap /= 2

    summation = sub_weight - (max_w_plus_1*cap)
    s.add(summation > gt)
    
    #if you cannot create an independent set with greater capacity than input, return false
    if s.check() == unsat:
        return False
    
    #else, model the set and calculate the value of the pb function
    m = s.model()
    cur_weight = 0
    for i in range(len(vars)):
        cur_weight += weights[i]*m[vars[i]].as_long()
    
    cur_cap = 0
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if i != j:
                cur_cap += graph[i][j] * m[vars[i]].as_long() * m[vars[j]].as_long()
    cur_summation = cur_weight - (max_w_plus_1*cur_cap)

    #recursively call the function, with this value as the new floor
    new_max = max_weight(cur_summation)
    
    #if you can't create an independent set with a greater weight, then this is the max weight independent set
    #so, return the model
    if new_max == False:
        vec = []
        for i in range(len(vars)):
            vec.append(m[vars[i]])
        return [vec, cur_summation]
    #otherwise return the greater weighted indepdendent set
    else:
        return new_max

max_w = max_weight(0)
if max_w == False:
    print("Independent set not found")

else:
    print("Max weight independent set found\nCharacteristic vector:", max_w[0], "\nWeight:", max_w[1])
