import sys
import string
import math

# Importing vocabulary into array of words with indices
vocab = []
i = 1
f = open('vocab.txt','r')
for line in f:
	vocab.append((i,line.rstrip('\n')))
	i = i+1
f.close()

print "Read vocab file"
# Import tokens of unigram into array
uni_count = []
i = 1
uni_total = 0
uni_count_copy = []
f = open('unigram.txt','r')
for line in f:
	count = int(line.rstrip('\n'))
	uni_count_copy.append(int(count))
	uni_count.append([int(i),int(count)])
	uni_total = uni_total + count
	i=i+1
f.close()

# Calculating the unigram probabilities for each token
unigram = []
log_unigram = []
for uni in uni_count:
	unigram.append([int(uni[0]),uni[1]/float(uni_total)])
	log_unigram.append([int(uni[0]),math.log(uni[1]/float(uni_total))])


# (a) printing table of words that start with 'a'
print "(a) printed words that start with a"
token = 'A'
words_with_a = []
for word in vocab:
	if word[1].startswith(token,0,len(word[1])):
		unigram_word = unigram[(word[0])]
		words_with_a.append([word[1], unigram_word[1]])
print words_with_a

# Import bigram into array
bi_count = []
n = 1
f = open('bigram.txt','r')
for line in f:
	i, j, count = line.rstrip('\n').split('\t')
	bi_count.append([int(i),int(j),int(count)])
	n = n+1
f.close()

# Calculating the bigram values
sum_list = []
j = len(uni_count_copy)
res = 0

# Finding the MLEs of bigram distribution 
bigram = []
log_bigram = []
for m,n,value in bi_count:
	for j,token in enumerate(uni_count_copy):
		if(m == j):
			if(token == 0):
				bigram.append([m,n,0])
				log_bigram.append([m,n,0])
				break
			else:
				bigram.append([m,n,(value/float(token))])
				log_bigram.append([m,n,math.log(value/float(token))])
				break

#(b) printing the bigram distribution for words after 'the'
print "(b) printed top 10 most likely words after token - the"
token_2 = 'THE'
words_after_token = []
for word in vocab:
	if word[1] == token_2:
		token_number = int(word[0])
for i,j,pbty in bigram:
	if (i == token_number):
		word_1 = vocab[i-1]
		word_2 = vocab[j-1]
		words_after_token.append([word_1[1],word_2[1],pbty])
words_after_token.sort(key=lambda tup: tup[2], reverse = True)
for i in range(0,10):
	print words_after_token[i]

#Parsing a sentence
parse_1 = 'The stock market fell by one hundred points last week.'
parse_2 = 'The sixteen officials sold fire insurance.'
parse_1 = parse_1.strip('\n').strip('.').upper()
parse_2 = parse_2.strip('\n').strip('.').upper()
uni_parse_1 = parse_1.split(' ')
uni_parse_2 = parse_2.split(' ')
#print uni_parse_1

bi_parse_1 = uni_parse_1
bi_parse_1.insert(0,'<s>')
bi_parse_2 = uni_parse_2
bi_parse_2.insert(0,'<s>')
#print bi_parse_1

# (c) Calculating the unigram log probability of the sentence
uni_parse_1_logtotal = 0
for token in uni_parse_1:
	for word in vocab:
		if (word[1] == token):
			token_number = int(word[0])
			log_val = log_unigram[token_number-1]
			uni_parse_1_logtotal += log_val[1]
print "(c) log likelihood of using unigram model = "+ str(uni_parse_1_logtotal)

# (c) Calculating the bigram log probability of the sentence
token_num_1 = 0
token_num_2 = 0
bi_parse_1_logtotal = 0
pairs = []
for token_1 in bi_parse_1:
	for word in vocab:
		if (word[1] == token_1):
			token_num_1 = int(word[0])
			if(token_num_2==0):
				token_num_2 = token_num_1
				break
			pairs.append([token_num_1,token_num_2])
			token_num_2 = token_num_1

for token_num_1,token_num_2 in pairs:
	for i,j,log_prob in log_bigram:
		if(i== token_num_1):
			if(j== token_num_2):
				bi_parse_1_logtotal += log_prob
print "(c) log likelihood of using bigram model = "+str(bi_parse_1_logtotal)
print "(c) the bigram model has the highest log likelihood"
# (d) Calculating the unigram log probability of the sentence
uni_parse_2_logtotal = 0
for token in uni_parse_2:
	for word in vocab:
		if (word[1] == token):
			token_number = int(word[0])
			log_val = log_unigram[token_number-1]
			uni_parse_2_logtotal += log_val[1]
print "(d) log likelihood of using unigram model = "+ str(uni_parse_2_logtotal)

#(d) Calculating the log bigram probability of the sentence
token_num_1 = 0
token_num_2 = 0
bi_parse_2_logtotal = 0
pairs = []
actualpairs = []
for token_2 in bi_parse_2:
	for word in vocab:
		if (word[1] == token_2):
			token_num_1 = int(word[0])
			if(token_num_2==0):
				token_num_2 = token_num_1
				break
			pairs.append([token_num_1,token_num_2])
			token_num_2 = token_num_1
for token_num_1,token_num_2 in pairs:
	for i,j,log_prob in log_bigram:
		if(i== token_num_1):
			if(j== token_num_2):
				bi_parse_2_logtotal += log_prob
				actualpairs.append([token_num_1,token_num_2])
print "(d) log likelihood of using bigram model = "+str(bi_parse_2_logtotal)

# The actual pairs of words which influnce the log likelihood of the sentence
for value in actualpairs:
	token_num_1 = value[0]
	#print token_num_1
	token_num_2 = value[1]
	#print token_num_2
	word_1 = vocab[token_num_1-1]
	word_2 = vocab[token_num_2-1]
	print "(d) The words that follow each other that actually appear on the training corpus are " + word_2[1], word_1[1]
	print "(d) Words that dont appear on the training corpus reduce the probability of the event occuring"

#(e) Calculating the lambda for the mixture model
param = 0
for param in range(0,11):
	token_num_1 = 0
	token_num_2 = 0
	m_parse_logtotal = 0
	for token_num_1,token_num_2 in pairs:
		for i,j,prob in bigram:
			if(i== token_num_1):
				if(j== token_num_2):
					unigram_pbty = unigram[token_num_2-1]
					m_parse_logtotal += math.log(float((1-(param*0.1))*unigram_pbty[1])+float((param*0.1)*prob))
	print "(e) lambda value = " + str(param*0.1) + " Log likelihood in mixture model = " +str(m_parse_logtotal)
	param += 1
