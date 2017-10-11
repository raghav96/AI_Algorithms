import sys
import math
import string
#import mathplotlib.pyplot as plt

# Importing the values of initial state distribution(pi)
pi = []
i = 1
f = open('C:/Users/ragha/OneDrive/Documents/Workspace/CSE150/initialStateDistribution.txt','r')
for line in f:
	pi.append(line.rstrip('\n'))
	i = i+1
f.close()
#print pi

#Importing the values of the emission matrix(bij)
b_ij = []
i = 1
f = open('C:/Users/ragha/OneDrive/Documents/Workspace/CSE150/emissionMatrix.txt','r')
for line in f:
	b_ij.append(line.rstrip('\n').split('\t'))
	i = i+1
f.close()
#print b_ij
# Importing the values of the transition matrix(aij)
a_ij = []
i = 1
f = open('C:/Users/ragha/OneDrive/Documents/Workspace/CSE150/transitionMatrix.txt','r')
for line in f:
	a_ij.append(line.rstrip(' \n').split(' '))
	i = i+1
f.close()

# Importing the values of the observations
obs = []
i = 1
f = open('C:/Users/ragha/OneDrive/Documents/Workspace/CSE150/observations.txt','r')
for line in f:
	obs.append(line.rstrip(' \n').split(' '))
	i = i+1
f.close()

t = len(obs[0])
print t

l_it = []
lit = []
for i in range(26):
	l_i1 = 0
	# o(t) becomes o(1)
	t = obs[0]
	t = t[0]
	#print t
	#for t in obs[0]:
	if (int(t)==0):
		bij = b_ij[i]
		bij = float(bij[0])
		init = float(pi[i])
		l_i1 += math.log(init) + math.log(bij)
		#print 0
	if (int(t)==1):
		#print 1
		bij = b_ij[i]
		bij = float(bij[1])
		init = float(pi[i])
		l_i1 += math.log(init) + math.log(bij)
	#print l_i1
	l_it.append(l_i1)
lit.append(l_it)
print "Calculated l_i1"

for t in obs[0]:
	if t==0:
		continue;
	l_in = []
	aij = 0 
	bij = 0
	t_val = int(t[0])
	# Loop for adding values to li(t+1)* = li(t) + aij + bik 
	for i in range(26):
		if(t_val == 0):
			l_in = []
			# Calculating bik based on i, k=0(t)
			bij = b_ij[i]
			bik = float(bij[0])
			for j in range(1,26):
				l_value = 0
				aij = a_ij[i]
				aij = float(aij[j])
				l_value = l_it[i] + math.log(aij) + math.log(bik)
				#print l_value
				l_in.append(l_value)
			l_it[i] = max(l_in)
			#print l_it[i]
		if(t_val == 1):
			l_in= []
			# Calculating bij based on i and k=0(t)
			bij = b_ij[i]
			bik = float(bij[1])
			for j in range(1,26):
				aij = a_ij[i]
				aij = float(aij[j])
				l_value = l_it[i] + math.log(aij) + math.log(bik)
				l_in.append(l_value)
			l_it[i] = max(l_in)
			#l_it += math.log(init) + math.log(bij)
		#print t_val
		lit.append(l_it)
print "Calculated lit matrix"

s = []
t = 54000
while (t != 0):
	if (t==54000):
		s_val = max(lit[t])
		s_i = lit[t].index(s_val)
		s.append([t,s_i])
	else:
		l_vals = lit[t]
		s_in = []
		j = s_i
		for i in range(26):
			aij = a_ij[i]
			aij = float(aij[j])
			s_value = l_vals[i] + math.log(aij)
			s_in.append(s_value)
		s_i = s_in.index(max(s_in))
		s.append([t,s_i])
	t = t-1
print s
#plt.plot(s)
#plt.ylabel('s_value')
#plt.show()




