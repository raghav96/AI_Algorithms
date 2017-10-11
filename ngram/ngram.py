import sys
import re
import math
from collections import defaultdict
from operator import itemgetter

#Statistical language modeling using N_gram model 
class NGram:
	def __init__(self):
		self.vocab = []
		self.unigram_prob = {}
		self.log_unigram = {}
		self.ngram_prob = {}
		self.log_ngram = {}


	def corpus(self, input_file):
		values = []
		f = open(input_file, 'r')
		for line in f:
			words = re.findall(r'\w+[\']\w+|\w+', line.upper())
			values.extend(words)
		return values

	def split_ngram(self, values, n):
		return [values[i:i+n] for i in range(len(values)-(n-1))]

	def parse(self, values, n, n_filter):
		uni_counts = dict()
		vocab = []
		for value in values:
			if value not in uni_counts:
				uni_counts[value] = 1
			else:
				uni_counts[value] += 1
		#print counts
		#for word in uni_counts.keys():
		#	if uni_counts[word] <= n_filter:
		#		uni_counts.pop(word)

		vocab = uni_counts.keys()
		total = sum(uni_counts.values())

		ngram_probs = []
		ngram_i = self.split_ngram(values, n)
		n_counts = dict()
		for word_set in ngram_i:
			if tuple(word_set) not in n_counts:
				n_counts[tuple(word_set)] = 1
			else:
				n_counts[tuple(word_set)] += 1

		#for word_set in n_counts.keys():
		#	if n_counts[word_set] <= n_filter:
		#		n_counts.pop(word_set)

		return vocab, uni_counts, n_counts, total

	def calc_probabilities(self, vocab, counts, ngram_counts, total):
		unigram_prob = {}
		log_unigram = {}
		for uni in uni_counts:
			unigram_prob[uni] = counts[uni]/float(total)
			log_unigram[uni] = math.log(counts[uni]/float(total))

		# Finding the MLEs of bigram distribution 
		ngram_prob = {}
		log_ngram = {}
		for key_set in ngram_counts:
			value = ngram_counts[key_set]
			c = counts[key_set[0]]
			ngram_prob[key_set] = value/float(c)
			log_ngram[key_set] = math.log(value/float(c))

		self.unigram_prob = unigram_prob
		self.log_unigram = log_unigram
		self.ngram_prob = ngram_prob
		self.log_ngram = log_ngram
		self.vocab = unigram_prob.keys()

		return self.unigram_prob, self.log_unigram, self.ngram_prob, self.log_ngram


	def word_starts_with(self, token, n):
		token = token.upper()
		words_with_token = []
		for word in self.vocab:
			if word.startswith(token,0,len(word)):
				unigram_word = self.unigram_prob[word]
				words_with_token.append((word, unigram_word))
		words_with_token = sorted(words_with_token, key=itemgetter(1))
		return words_with_token[0:n]

	def word_that_follows(self, prev_word, n):
		prev_word = prev_word.upper()
		token_2 = prev_word
		words_after_token = []
		for word_set in self.ngram_prob.keys():
			pbty = self.ngram_prob[word_set]
			if (word_set[0] == token_2):
				words_after_token.append((word_set, pbty))
		words_after_token = sorted(words_after_token, key=itemgetter(1))
		return words_after_token[0:n]

	def calculate_sentence(self, sentence):
		p_sentence = re.findall(r'\w+[\']\w+|\w+', sentence.upper())

		# Unigram probability of sentence
		sent_log_prob = 0
		for word in p_sentence:
			if word in self.vocab:
				log_val = self.log_unigram[word]
				sent_log_prob += log_val

		n_split = len(self.ngram_prob.keys()[0])

		p_sentence = self.split_ngram(p_sentence, n_split)

		# Ngram probabability of sentence
		sent_log_n = 0
		for word_set in p_sentence:
			if tuple(word_set) in self.log_ngram.keys():
				log_val = self.log_ngram[tuple(word_set)]
				sent_log_n += log_val

		# Mixture model probability of sentence, averaging values over
		# both unigram and n_gram model
		mix = {}
		for param in range(0, 10):
			for word_set in p_sentence:
				word = word_set[0]
				if word in self.vocab:
					uni_prob = self.unigram_prob[word]
					n_prob = self.ngram_prob[tuple(word_set)]
					if(param not in mix.keys()):
						mix[param] = 0
					mix[param] += math.log(float((1-(param*0.1))*uni_prob)+float((param*0.1)*n_prob))

		mix_model_log = sum(mix.values())/len(mix.values())
		return sent_log_prob, sent_log_n, mix_model_log

	def finish_sentence(self, sentence, n):
		p_sentence = re.findall(r'\w+[\']\w+|\w+', sentence.upper())
		next_word = p_sentence[-1]
		sentence = [next_word]
		if next_word in self.vocab:
			counter = 0
			while counter <= n:
				word_ngrams = []
				for word_set in self.ngram_prob:
					if word_set[0] == next_word and (word_set[-1] not in sentence):
						word_ngrams.append((word_set, self.ngram_prob[word_set]))
				top_pair = sorted(word_ngrams, key=itemgetter(1))[-1]
				next_word = top_pair[0][1]
				counter += 1
				sentence.append(next_word)

		return sentence;
		
ngram = NGram()
words = ngram.corpus('warandpeace.txt')
n_filter = 1
vocab, uni_counts, bi_counts, total = ngram.parse(words, 4, n_filter)
ngram.calc_probabilities(vocab, uni_counts, bi_counts, total)
print ngram.word_starts_with('A', 10)
print ngram.word_that_follows('MAKE', 10)
print ngram.calculate_sentence('Can one be well while suffering morally?')
print ngram.finish_sentence('Man', 20)


