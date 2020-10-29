from z3 import *

raw_data = open('input', 'r')
data_content = raw_data.readlines()

#read in the variables from the input file
in_a = int(data_content[0][:data_content[0].index('\n')])
m = int(data_content[1][:data_content[1].index('\n')])
in_b = int(data_content[2][:data_content[2].index('\n')])
n = int(data_content[3])

#setting up out_a with initial out_a = in_a
pow_a = [in_a]

#setting up out_b with initial out_b = in_b
pow_b = [in_b]

#implementation of power
for i in range(1,m+1):
    pow_a.append(pow_a[i-1]*in_a)

#implementation of power_new
for i in range(1, n+1):
    pow_b.append(pow_b[i-1]*pow_b[i-1])


#checking that the final out_a == final out_b
psi = (pow_a[-1] == pow_b[-1])


s: Solver = Solver()


s.add(psi)
if s.check() == sat:
    print("true")
elif s.check() == unsat:
    print("false")
