# hw3.py CSE 150 Winter 2017
# Prof. Kamalika Chaudhari
# Team Members:
# Raghav Ravisankar A99115039
# Kedar Pujara A99123184
# Josh Rudolph A11626995
#
# Please ensure the hw3 txt files are in /data/ folder

import sys
import numpy as np
import math
import string


#Initializing variables 
features = []
train_data = []
test_data = []
valid_data = []
target = "LIMIT_BAL"

# Path names for the files
train_file = "/Users/raghav/Documents/workspace/cse151/hw3/data/hw3train.txt"
test_file = "/Users/raghav/Documents/workspace/cse151/hw3/data/hw3test.txt"
validate_file = "/Users/raghav/Documents/workspace/cse151/hw3/data/hw3validate.txt"
features_file = "/Users/raghav/Documents/workspace/cse151/hw3/data/hw3features.txt"

class Node:
    label = ""
    values = []
    
    def __init__(self, val, dictionary):
        self.label = val
        if(isinstance(dictionary, dict)):
            self.values = dictionary.keys()
    
    def getLabel(self):
        return self.label
        
def main():
	# Inintializing data into lists
	f = open(features_file,'r')
	for line in f:
		line = line.strip("\r\n")
		features.append(line.split(' '))

	f = open(train_file,'r')
	for line in f:
		line = line.strip(" \r\n")
		train_data.append(line.split(' '))

	f = open(test_file,'r')
	for line in f:
		line = line.strip(" \r\n")
		test_data.append(line.split(' '))

	f = open(train_file,'r')
	for line in f:
		line = line.strip(" \r\n")
		valid_data.append(line.split(' '))

	# Creating a tree for the 
	tree_dict = Tree.create_tree(train_data, features, target, 0)
	data = train_data
	for rec in data:
		# Copying the subset of the data into the tree
		node_dict = tree_dict.copy()
		result = ""
		# checking if the instance is dict and finding the value
		# for the particular feature in the dataset
		# Setting the root of the tree
		while(isinstance(node_dict, dict)):
			val = node_dict.keys()[0]
			root = Node.Node(val, node_dict[val])
			node_dict = node_dict[val]

			#Find index of the selected feature and get its value
			idx = features.index(target)
			feature_val = rec[idx]

		# Creating children based on the features in node_dict
		if (feature_val in node_dict.keys()):
			child = Node.Node(feature_val, node_dict[feature_val])
			result = node_dict[feature_val]
			node_dict = node_dict[feature_val]
		
		else:
			print "cannot process input"
			result = "?"
			break

		print ("entry " + count + " =" + result)



class Tree:
	# Function that gets data and features and returns
	# the target feature which gives the max gain in entropy
	# so that the entropy of the data can be reduced
	# by the splitting rule
	def choose_target(self, data, features, target):
		# Initializing target label and max_gain values
		target_label = features[0]
		max_gain = 0;
		# Iterating through the features to find the optimal
		# feature
		for target_feature in features:
			# Calculating the gain for each feature
			feature_gain = calculate_gain(data, features, target_feature, target)
			# Updating the max_gain to get feature with max gain
			if feature_gain> max_gain:
				max_gain = feature_gain
				target_label = target_feature
		return target_label

	def calculate_gain(self, data, features, target_feature, target):
		# Initializing values for freq and entropy along each feature
		freq = {}
		feature_entropy = 0.0

		#Find index of the selected feature
		idx = features.index(target)

		# Adds to frequency of each of the values to the freq vector
		for record in data:
			if (freq.has_key(record[i])):
				freq[record[i]] += 1.0;
	        else:
	        	freq[record[i]]  = 1.0;
	    
	    # Gain = entropy of features - probability of feature * entropy(subset_data of feature)
	    # Calculates the gain of the specific feature
	    
		for value in freq.keys():
			value_prob = (freq[value] / sum(freq.values()))
			subset_data = [x for x in data if x[i] == value]
			feature_entropy += value_prob*entropy(subset_data, features, target_feature, target)

	   	return (entropy(subset_data, features, target_feature, target) - feature_entropy)

	def entropy(self, data, features, target_feature, target):
		freq = {}
		entropy_value = 0.0

		# Find index of target attribute
		idx = features.index(target)

		# Calculate the frequency of each of the values in the target attr
		for entry in data:
			if (freq.has_key(entry[i])):
				freq[entry[i]] += 1.0;
			else:
				freq[entry[i]]  = 1.0;

		# Calculate the entropy of the data for the target feature
		for freq in freq.values():
			entropy_value += (-freq/len(data)) * math.log(freq/len(data), 2)

		return entropy_value


	# Function that returns the most common label given the subset of data
	def most_common(self, data, features, target):
		# Frequency vector
		freq = {}
		#Find index of the selected feature
		idx = features.index(target)
		# Traversing through data
		for value in data:
			# Adding the frequency of the particular value
			if(freq.has_key(value[idx])):
				freq[value[idx]] += 1
			else:
				freq[value[idx]] = 1
		# Initializing variables for max_freq and most common label
		max_freq = 0
		common = ""
		# Traversing through the different values to get the
		# most common label
		for key in freq.keys():
			if freq[key] > max_freq:
				max_freq = freq[key]
				common = key
		return common

	def get_subset(self, data, features, target_feature, rec_val):
		# initializing the subset and the target idx
		subset = [[]]
		idx = features.index(target_feature)
		# Traversing through the data to get the values
		# not in the feature subset of the target index
		for rec in data:
			# finding entries that match value of feature
			if(rec[idx] == rec_val):
				# Adding the entries of the data which are not
				# part of the features
				entry = rec.pop(idx)
				subset.append(entry)
		subset.remove([])
		return subset

	def create_tree(self, data, features, target, recursion):
		recursion +=1
		# Decision tree 
		idx = features.index(target)
		# Fetches the values for target feature in dataset
		values = [x[idx] for x in data]
		# Finds the most common label amongst dataset
		default_label = most_common(data, features, target)

		# If the size of the dataset is 0, meaning the label
		# doesnt have any datapoints, or if the dataset has only
		# the target label, return label

		if len(data)==0 or (len(features)-1) == 0:
			return default_label

		# Checks if all the values in the dataset are same
		# and returns the value
		elif values.count(values[0]) == len(vals):
			return values[0]
		else:
			# Choose the next best feature to classify the subset
			# of data
			target_label = choose_target(data, features, target)
			decision_tree = {target_label:{}}

			# Finds out all the unique values of the 
			vals = [rec[features.index(target)] for rec in data]
			vals = list(set(vals))

			for val in vals:
				# Create a subset of the data for current target features
				subset = get_subset(data, features, target_feature, val)
				feature_subset = features.remove(target_label)
				feature_subtree = createTree(subset, feature_subset, target, recursion)

				# Add new subtree to decision subtree
				decision_tree[target_label][val] = feature_subtree

		return decision_tree






	




