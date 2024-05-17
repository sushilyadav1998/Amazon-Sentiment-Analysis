import sys
import re
import nltk
from gensim.models import Word2Vec
import os


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = ""
    if len(sys.argv) < 2:
        folder_path = input("Please provide the folder path: ")
    else:
        folder_path = sys.argv[1] + "/"

    reviews = []
    file_names = ["pos.txt", "neg.txt"]

    nltk.download("punkt")

    for file_name in file_names:
        with open(os.path.join(folder_path, file_name), "r") as file:
            for line in file:
                reviews.append(re.sub(r"\n", "", str(line)).lower())

    # print(f"Total reviews: {len(reviews)}")

    tokenized_reviews = [nltk.word_tokenize(str(review)) for review in reviews]

    model = Word2Vec(tokenized_reviews, min_count=20, vector_size=50)

    model.save(current_dir + '\data\w2v_50.model')

    print("20 most similar words to 'good':", model.wv.most_similar('good', topn=20))
    print("20 most similar words to 'bad':", model.wv.most_similar('bad', topn=20))


if __name__ == "__main__":
    main()
