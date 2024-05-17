import os
import sys
import pickle
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

if len(sys.argv) != 3:
    sys.exit(1)

input_file = sys.argv[1]
classifier_type = sys.argv[2]

stopword_str = ""
if "ns" in classifier_type:
    stopword_str = "ns"

if "uni" in classifier_type:
    feature_str = "uni"
elif "bi" in classifier_type:
    feature_str = "bi"
elif "uni_bi" in classifier_type:
    feature_str = "uni_bi"

if stopword_str:
    clf_filename = f"mnb_{feature_str}_{stopword_str}.pkl"
else:
    clf_filename = f"mnb_{feature_str}.pkl"
clf_filepath = os.path.join(os.getcwd(), 'data', clf_filename)
with open(clf_filepath, "rb") as f:
    clf = pickle.load(f)

if stopword_str:
    vec_filename = f"vectorizer_{feature_str}_{stopword_str}.pkl"
else:
    vec_filename = f"vectorizer_{feature_str}.pkl"
vec_filepath = os.path.join(os.getcwd(), 'data',  vec_filename)
with open(vec_filepath, "rb") as f:
    vectorizer = pickle.load(f)

sentences = []
with open(input_file, "r") as f:
    sentences = [line.strip() for line in f]

X = vectorizer.transform(sentences)

predictions = clf.predict(X)

for sentence, prediction in zip(sentences, predictions):
    if prediction == 1:
        print(f"{sentence}: Positive")
    else:
        print(f"{sentence}: Negative")
