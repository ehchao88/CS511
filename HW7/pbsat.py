from z3 import *
import sys
import ast

#taking input and converting to objective function and constraints
p = open(sys.argv[1], 'r')
p_lines = p.readlines()
problem = ""
for line in p_lines:
    problem += line.strip('\n')
problem = ast.literal_eval(problem)

#getting the objective function
obj_f = problem[0]

#getting constraint list
constraints = problem[1:]

#obj_f = [[1,[[0,1]]], [1,[[0,2]]]]

#get number of variables
max_var = 0
for addr in obj_f:
    for term in addr[1]:
        if term[1] > max_var:
            max_var = term[1]
#print(max_var)


#constraints = [
#   [ [1,[[0,1],[1,2]]], [2,[[0,2]]], [-3,[[0,1]]], [-1,[]] ] ,
#[ [-1,[[0,1],[1,2]]], [-2,[[0,2]]], [3,[[0,1]]], [1,[]] ]
#]

vars = ([Int('x'+str(i+1)) for i in range(max_var)])

#print(vars)
def pb_opt(constraints, obj_f):
    s = Solver()
    #variables must be in {0,1}
    for var in vars:
        s.add(Or(var == 0, var == 1))
    #build constraint functions from list of constraints
    for constraint in constraints:
        cur_func = 0
        for addr in constraint:
            mul = addr[0]
            for term in addr[1]:
                #do logical negation if indicated
                if [term][0] == 1:
                    mul *= (((vars[term[1]-1]*-1)+1))
                else:
                    mul *= vars[term[1]-1]
            cur_func += mul
        #add the current constraint to the solver
        s.add(cur_func <= 0)
    
    #check if sat with current constraints
    if s.check() == unsat:
        return False
    
    #find the model if it is satisfiable
    m = s.model()
    obj_f_value = 0

    #find the value of the objective function with the given model
    for addr in obj_f:
        mul = addr[0]
        for term in addr[1]:
            #do logical negation if indicated
            if [term][0] == 1:
                mul *= (((m[vars[term[1]-1]].as_long()*-1)+1))
            else:
                mul *= m[vars[term[1]-1]].as_long()
        obj_f_value += mul

    #create a new constraint, making the objective function less than the value of the objective function with the current model
    new_constraint = obj_f.copy()
    new_constraint.append([((obj_f_value-1)*-1), []])
    
    #add this new constraint the the list of constraints
    constraints.append(new_constraint)
    
    #find if still satisfiable with new constraint
    minimize = pb_opt(constraints, obj_f)

    #if still satisfiable, return the model given from adding the new constraint
    if minimize != False:
        return  minimize

    #if not satisfiable with the new constraint, return the current model
    return (True, s.model())

print(pb_opt(constraints, obj_f))
