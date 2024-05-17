# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 20:13:31 2023
@author: 15485
"""   
import sys
from gensim.models import Word2Vec
import os

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if len(sys.argv) < 2:
        word_file_path = input("Please provide the file path: ")
    else:
        word_file_path = sys.argv[1] + "/"
    
    model_path = os.path.join(current_dir, "data", "w2v.model")

    model = Word2Vec.load(model_path)
    
    words = []
    with open(word_file_path, "r") as file:
        for line in file:
            words.append(line.strip())
    
    for word in words:
        try:
            print("Top 20 words most similar to '", word, "':")
            similar_words = model.wv.most_similar(word, topn=20)
            for similar_word, similarity in similar_words:
                print(similar_word, ":", similarity)
        except KeyError:
            print("The word '", word, "' is not in the vocabulary.")
        finally:
            print("\n")

if __name__ == "__main__":
    main()
