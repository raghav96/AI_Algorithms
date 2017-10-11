import sys
import math
import string

a1 = []
a2 = []
a3 = []
a4 = []
r = []
gamma = 0.9925

# Importing the values of the probability for each s and s, west'
f = open('C:/Users/ragha/OneDrive/Documents/Workspace/CSE150/prob_a1.txt','r')
for line in f:
	a1_vals = line.rstrip('\n').split('   ')
	a1_vals.remove('')
	a1_vals[0] = int(a1_vals[0])
	a1_vals[1] = int(a1_vals[1])
	a1_vals[2] = float(a1_vals[2])
	a1.append(a1_vals)
f.close()
#print a1

# Importing the values of the probability for each s and s, north'
f = open('C:/Users/ragha/OneDrive/Documents/Workspace/CSE150/prob_a2.txt','r')
for line in f:
	a2_vals = line.rstrip('\n').split('   ')
	a2_vals.remove('')
	a2_vals[0] = int(a2_vals[0])
	a2_vals[1] = int(a2_vals[1])
	a2_vals[2] = float(a2_vals[2])
	a2.append(a2_vals)
f.close()


# Importing the values of the probability for each s and s for east'
f = open('C:/Users/ragha/OneDrive/Documents/Workspace/CSE150/prob_a3.txt','r')
for line in f:
	a3_vals = line.rstrip('\n').split('   ')
	a3_vals.remove('')
	a3_vals[0] = int(a3_vals[0])
	a3_vals[1] = int(a3_vals[1])
	a3_vals[2] = float(a3_vals[2])
	a3.append(a3_vals)
f.close()

# Importing the values of the probability for each s and s for south'
f = open('C:/Users/ragha/OneDrive/Documents/Workspace/CSE150/prob_a4.txt','r')
for line in f:
	a4_vals = line.rstrip('\n').split('   ')
	a4_vals.remove('')
	a4_vals[0] = int(a4_vals[0])
	a4_vals[1] = int(a4_vals[1])
	a4_vals[2] = float(a4_vals[2])
	a4.append(a4_vals)
f.close()


# Importing the values of the rewards for each s 
f = open('C:/Users/ragha/OneDrive/Documents/Workspace/CSE150/rewards.txt','r')
for line in f:
	r_vals = line.rstrip('\n')
	r_vals = float(int(r_vals))
	r.append(r_vals)
f.close()

q_val = [0.0 for j in range(4)]
v_vals = [q_val for k in range(81)]
v_best = [0.0 for k in range(81)]
for test in range(1000):
	for s in range(1,82):
		r_val = r[s-1]
		q_val = [j for j in range(4)]
		for a in range(4):
			a_vals = []
			#print a
			if a==0:
				a_vals = a1
			if a==1:
				a_vals = a2
			if a==2:
				a_vals = a3
			if a==3:
				a_vals = a4
			sum_pv = 0.0
			for a_val in a_vals:
				if(a_val[0]==s):
					s_p = a_val[1]
					v_sp = v_best[s_p-1]
					p_sp = a_val[2]
					sum_pv += v_sp*p_sp
			q_val[a] = sum_pv
		v_vals[s-1] = q_val
		v_best[s-1] = r_val + gamma*(max(q_val))

for i,v in enumerate(v_best):
	if (v!=0):
		print str(v) + " @indexof " + str(i+1)

for i,v in enumerate(v_vals):
	if (max(v_vals[i])==v_vals[i][0]):
		print "west "+ str(i+1)
	elif (max(v_vals[i])==v_vals[i][1]):
		print "north "+ str(i+1)
	elif (max(v_vals[i])==v_vals[i][2]):
		print "east "+ str(i+1)
	else:
		print "south "+ str(i+1)





