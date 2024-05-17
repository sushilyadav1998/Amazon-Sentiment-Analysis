import sys
import csv
import os
from gensim.models import Word2Vec
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import L2
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from tensorflow.keras.optimizers.schedules import ExponentialDecay

def get_sentence_embeddings(file_path, word2vec_model):
    sentences = []
    with open(file_path, 'r') as file:
        sentences = list(csv.reader(file, delimiter=','))
    
    word_embeddings = []
    for sentence in sentences:
        temp = []
        for word in sentence:
            if word in word2vec_model.wv:
                temp.append(word2vec_model.wv[word])
            else:
                temp.append([0.0] * word2vec_model.vector_size)
        word_embeddings.append(temp)
    return word_embeddings

def read_file(file_path):
    labels = []
    with open(file_path, 'r') as file:
        labels = list(csv.reader(file, delimiter=','))
    
    label_array = []
    for sublist in labels:
        for item in sublist:
            label_array.append(int(item))
    return to_categorical(np.asarray(label_array))

def relu_func(train_data, train_labels, val_data, val_labels, test_data, test_labels):
    model = Sequential()
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(2, activation='softmax', kernel_regularizer=L2(0.1)))
    lr_schedule = ExponentialDecay(
        initial_learning_rate=1e-3,
        decay_steps=100,
        decay_rate=0.9
    )
    opt = Adam(learning_rate=lr_schedule)
    model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
    model.fit(train_data, train_labels, epochs=15, batch_size=1000, validation_data=(val_data, val_labels))
    _, accuracy = model.evaluate(test_data, test_labels)
    print('Accuracy: %.2f' % (accuracy * 100))
    model.save(os.path.join(input_dir, 'nn_relu.model.h5'))

def sigmoid_func(train_data, train_labels, val_data, val_labels, test_data, test_labels):
    model = Sequential()
    model.add(Flatten())
    model.add(Dense(512, activation='sigmoid'))
    model.add(Dropout(0.25))
    model.add(Dense(2, activation='softmax', kernel_regularizer=L2(0.1)))
    lr_schedule = ExponentialDecay(
        initial_learning_rate=1e-3,
        decay_steps=100,
        decay_rate=0.9
    )
    opt = Adam(learning_rate=lr_schedule)
    model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
    # model.compile(loss='binary_crossentropy', optimizer=Adam(0.001), metrics=['accuracy'])
    model.fit(train_data, train_labels, epochs=15, batch_size=1000, validation_data=(val_data, val_labels))
    _, accuracy = model.evaluate(test_data, test_labels)
    print('Accuracy: %.2f' % (accuracy * 100))
    model.save(os.path.join(input_dir, 'nn_sigmoid.model.h5'))

def tanh_func(train_data, train_labels, val_data, val_labels, test_data, test_labels):
    model = Sequential()
    model.add(Flatten())
    model.add(Dense(512, activation='tanh'))
    model.add(Dropout(0.25))
    model.add(Dense(2, activation='softmax', kernel_regularizer=L2(0.1)))
    lr_schedule = ExponentialDecay(
        initial_learning_rate=1e-3,
        decay_steps=100,
        decay_rate=0.9
    )
    opt = Adam(learning_rate=lr_schedule)
    model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
    # model.compile(loss='binary_crossentropy', optimizer=Adam(0.001), metrics=['accuracy'])
    model.fit(train_data, train_labels, epochs=15, batch_size=1000, validation_data=(val_data, val_labels))
    _, accuracy = model.evaluate(test_data, test_labels)
    print('Accuracy: %.2f' % (accuracy * 100))
    model.save(os.path.join(input_dir, 'nn_tanh.model.h5'))



def main():
    model = Word2Vec.load(os.path.join(input_dir, 'word2vec.model'))

    train_data = get_sentence_embeddings(os.path.join(input_dir, 'train.csv'), model)
    test_data = get_sentence_embeddings(os.path.join(input_dir, 'test.csv'), model)
    val_data = get_sentence_embeddings(os.path.join(input_dir, 'val.csv'), model)

    train_labels = read_file(os.path.join(input_dir, 'train.labels.csv'))
    test_labels = read_file(os.path.join(input_dir, 'test.labels.csv'))
    val_labels = read_file(os.path.join(input_dir, 'val.labels.csv'))

    length = [len(s) for s in (train_data + test_data + val_data)]
    max_length = max(length)

    train_data = pad_sequences(train_data, maxlen=max_length, padding='post', truncating='post')
    test_data = pad_sequences(test_data, maxlen=max_length, padding='post', truncating='post')
    val_data = pad_sequences(val_data, maxlen=max_length, padding='post', truncating='post')

    relu_func(train_data, train_labels, val_data, val_labels, test_data, test_labels)
    sigmoid_func(train_data, train_labels, val_data, val_labels, test_data, test_labels)
    tanh_func(train_data, train_labels, val_data, val_labels, test_data, test_labels)
    
if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = ""
    if len(sys.argv) < 2:
        input_dir = input("Please provide the folder path: ")
    else:
        input_dir = sys.argv[1] + "/"
    main()
