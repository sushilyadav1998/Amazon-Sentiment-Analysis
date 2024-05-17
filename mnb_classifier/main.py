import os
import numpy as np
import pandas as pd
import re
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
import warnings
import sys
import pickle

ans = []

train, val, test, train_l, val_l, test_l, train_s, val_s, test_s = [], [], [], [], [], [], [], [], []

def load(filename, arr, isLabel):
    f = open(filename, "r")
    for i in f:
        st = re.sub(r"\[|\]|\,|\'|\n", '', i)
        if isLabel:
            arr.append(int(st))
        else:
            arr.append(st)
    f.close()

def load_input_data():
    load(input_data + "train.csv", train, False)
    load(input_data + "val.csv", val, False)
    load(input_data + "test.csv", test, False)
    load(input_data + "train_labels.txt", train_l, True)
    load(input_data + "val_labels.txt", val_l, True)
    load(input_data + "test_labels.txt", test_l, True)
    load(input_data + "train_stop.csv", train_s, False)
    load(input_data + "val_stop.csv", val_s, False)
    load(input_data + "test_stop.csv", test_s, False)

def vectorize_data(kind, tr, va, te):
    if kind == 1:
        vectorizer = CountVectorizer(ngram_range=(1, 1))
    elif kind == 2:
        vectorizer = CountVectorizer(ngram_range=(2, 2))
    elif kind == 3:
        vectorizer = CountVectorizer(ngram_range=(1, 2))
    else:
        pass
    X_train = vectorizer.fit_transform(tr)
    X_val = vectorizer.transform(va)
    X_test = vectorizer.transform(te)
    return X_train, X_val, X_test, vectorizer

def train_model(X_train, X_val):
    alpha = [0, 0.1, 0.2, 0.5, 1, 10, 20, 50, 100]
    maxi = 0
    hyper = 0
    for i in alpha:
        clf = MultinomialNB(alpha=i)
        clf.fit(X_train, train_l)
        y_pred = clf.predict(X_val)
        score = accuracy_score(val_l, y_pred)
        if score > maxi:
            maxi = score
            hyper = i
    return hyper


def test_model(hyper, X_train, X_test, type1, type2, vectorizer):
    clf = MultinomialNB(alpha=hyper)
    clf.fit(X_train, train_l)
    y_pred = clf.predict(X_test)
    score = accuracy_score(test_l, y_pred)
    s = ""
    if not type1:
        s = s + "Without Stop Words; "
    else:
        s = s + "With Stop Words; "
    if type2 == 1:
        s = s + "Unigrams; Test Accuracy = "
    elif type2 == 2:
        s = s + "Bigrams; Test Accuracy = "
    elif type2 == 3:
        s = s + "Unigrams + Bigrams; Test Accuracy = "
    s = s + str(score * 100) + "%"
    ans.append(s)

    # Save the classifier and vectorizer
    if not type1:
        stopword_str = "ns"  # No stop words
    else:
        stopword_str = ""  # With stop words
    if type2 == 1:
        feature_str = "uni"  # Unigrams
    elif type2 == 2:
        feature_str = "bi"  # Bigrams
    elif type2 == 3:
        feature_str = "uni_bi"  # Unigrams + Bigrams

    # Save classifier
    if stopword_str:
        clf_filename = f"mnb_{feature_str}_{stopword_str}.pkl"
    else:
        clf_filename = f"mnb_{feature_str}.pkl"
    clf_filepath = os.path.join(current_dir, 'data',  clf_filename)
    with open(clf_filepath, "wb") as f:
        pickle.dump(clf, f)

    # Save vectorizer
    if stopword_str:
        vec_filename = f"vectorizer_{feature_str}_{stopword_str}.pkl"
    else:
        vec_filename = f"vectorizer_{feature_str}.pkl"
    vec_filepath = os.path.join(current_dir, 'data', vec_filename)
    with open(vec_filepath, "wb") as f:
        pickle.dump(vectorizer, f)

def no_stop_model():
    for i in range(1, 4):
        X_train, X_val, X_test, vectorizer = vectorize_data(i, train, val, test)
        hyper = train_model(X_train, X_val)
        test_model(hyper, X_train, X_test, False, i, vectorizer)


def stop_model():
    for i in range(1, 4):
        X_train, X_val, X_test, vectorizer = vectorize_data(i, train_s, val_s, test_s)
        hyper = train_model(X_train, X_val)
        test_model(hyper, X_train, X_test, True, i, vectorizer)

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    warnings.filterwarnings("ignore")
    input_data = ""
    if len(sys.argv) < 2:
        input_data = input("Please provide the folder path: ")
    else:
        input_data = sys.argv[1] + "/"
    load_input_data()
    ans = []
    no_stop_model()
    stop_model()

    for i in ans:
        print(i)
