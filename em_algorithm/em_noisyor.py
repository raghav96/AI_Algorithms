import sys
import string
import math

# Analysis on some portion of dataset http://archive.ics.uci.edu/ml/datasets/SPECT+Heart
# Dataset provided by Prof. Saul Lawrence, UCSD
# Implementing the EM algorithm on 
# Importing the values of x
x_values = []
f = open('hw6_x.txt','r')
for line in f:
	x_values.append(line.rstrip(' \n').split())
f.close()

#Importing the values of y
y_values = []
f = open('hw6_y.txt','r')
for line in f:
	y_values.append(line.rstrip('\n'))
f.close()

# Length of the data
t = int(len(x_values))

#Length of x
n = int(len(x_values[0]))
#print n

log_y= []
logval_y = 0

old_cpt = [1.0/46 for i in range(n)]
new_cpt = [1.0/46 for i in range(n)]
for i in range(0,513):
	ix_2 = 0
	mistake = 0
	# Calculating p(y=1|x'), len = 237
	cpt_y = []
	for x in x_values:
		# Looping through each x vector to calculate p(y=1|x')
		cpt = 1
		ix = 0
		for xi in x:
			# Adding the probabilities of the values of pi for each xi
			cpt =cpt*(1-(float(xi)*float(new_cpt[ix])))
			ix += 1
		cpt_y.append(1-cpt)

	for cpt in new_cpt:
		num = 0
		# Calculating ti for each of the i values
		ti = 0
		ti_factor = 0
		for x in x_values:
			if(int(x[ix_2])==1):
				ti += 1
		# Traversing through t to get yt and xit
		for t in range(267):
			# Calculating yt and xit
			y_value = y_values[t]
			x_set = x_values[t]
			x_value = x_set[ix_2]
			# Calculating the 1/ti element in equation
			if(ti !=0):
				ti_factor = float(1.0/ti)
			# Calculating the factor for new pi
			num += ti_factor*float(x_value)*float(y_value)/float(cpt_y[t])
		# Updating the new pi
		new_cpt[ix_2] = num*float(new_cpt[ix_2])
		ix_2+=1
	#print new_cpt
	logval_y = 0
	ti_factor = 0
	if(ti !=0):
		ti_factor = (1.0/ti)
	t = 0
	for y in y_values:
		if (int(y)==1):
			if (cpt_y[t]<=0.5):
					mistake += 1
			logval_y += ti_factor*math.log(cpt_y[t])
		if (int(y)==0):
			if (cpt_y[t]>=0.5):
					mistake += 1
			logval_y += ti_factor*math.log((1-cpt_y[t]))
		t += 1
	#print mistake
	if i in (0,1,2,4,8,16,32,64,128,256,512):
		print "Iteration:", i, "\tMistakes done by algorithm:", mistake, "\tConditional log-likelihood:", logval_y, "\n"
