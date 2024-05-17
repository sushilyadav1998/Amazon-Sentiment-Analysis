# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 22:51:25 2023

@author: 15485
"""

from gensim.models import Word2Vec
import multiprocessing
import random
import sys

special_characters = '[\'\",.-?!"#$%&(*)+/:;<=>@\[\]\\\\^`{|}~\t\n]+' 

def tokenize(text, characters):
	# Remove the special characters
	for c in characters:
		text = text.replace(c," ")     
	# Split into tokens
	# Normalize to lower case
	tokens = text.lower().split()
	return tokens

def load_data(file_path):
	with open (file_path + "pos.txt") as f:
		pos_lines = f.readlines()
	with open (file_path + "neg.txt") as f:
		neg_lines = f.readlines()
	data = []
	for line in pos_lines:
		tokens = tokenize(line, special_characters)
		data.append(tokens)
	for line in neg_lines:
		tokens = tokenize(line, special_characters)
		data.append(tokens)
	random.shuffle(data)
	return data

def main(file_path):
	# Train a word2vec model on the given data set

	data = load_data(file_path)
	# Count the number of cores in a computer
	cores = multiprocessing.cpu_count()
	w2v_model = Word2Vec(data, vector_size = 100, window = 5, min_count = 1, workers = cores-1)
	w2v_model.save(file_path + "w2v_new.model")
	print("Good similar:{}".format(w2v_model.wv.similar_by_word("good", 20)))
	print("Bad similar:{}".format(w2v_model.wv.similar_by_word("bad", 20)))



if __name__ == "__main__":
	main(sys.argv[1])