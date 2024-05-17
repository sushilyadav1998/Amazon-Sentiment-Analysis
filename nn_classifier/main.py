import os
import sys
import re
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import accuracy_score
from gensim.models import Word2Vec
from torch.nn.utils.rnn import pad_sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
import numpy as np
import csv

class Classifier(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes, dropout_rate):
        super(Classifier, self).__init__()
        self.hidden_layer = nn.Linear(input_size, hidden_size)
        self.output_layer = nn.Linear(hidden_size, num_classes)
        self.dropout = nn.Dropout(dropout_rate)
        self.activation = nn.ReLU()  # Change the activation function here

    def forward(self, x):
        x = x.to(torch.float32)
        x = self.hidden_layer(x)
        x = self.activation(x)
        x = self.dropout(x)
        x = torch.nn.functional.softmax(self.output_layer(x), dim=2)  # Apply softmax activation
        return x

# def load_data(file_path, is_label):
#     arr = []
#     with open(file_path, 'r') as file:
#         for line in file:
#             line = re.sub(r"\[|\]|\,|\n'", '', line)
#             if is_label:
#                 arr.append(int(line))
#             else:
#                 arr.append(line.split())
#     return arr

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

# input_dir = r'C:\Users\15485\Desktop\UWaterloo_Academics\MSCI641\Assignments_conda\a2\data'
# w2v_model = Word2Vec.load(os.path.join(input_dir, 'w2v.model'))

# train_data = load_data(os.path.join(input_dir, 'train_stop.csv'), False)
# val_data = load_data(os.path.join(input_dir, 'val_stop.csv'), False)
# test_data = load_data(os.path.join(input_dir, 'test_stop.csv'), False)
# train_labels = load_data(os.path.join(input_dir, 'train_labels.txt'), True)
# val_labels = load_data(os.path.join(input_dir, 'val_labels.txt'), True)
# test_labels = load_data(os.path.join(input_dir, 'test_labels.txt'), True)

# def load_data(file_path, is_label):
#     arr = []
#     with open(file_path, 'r') as file:
#         for line in file:
#             line = re.sub(r"[\[\],\n']", '', line)
#             if is_label:
#                 arr.append(int(line))
#             else:
#                 arr.append(line.split())
#     return arr

# def get_sentence_embeddings(sentences, w2v_model):
#     embeddings = []
#     for sentence in sentences:
#         sentence_embeddings = []
#         for word in sentence:
#             # print(word)
#             if word in w2v_model.wv:
#                 sentence_embeddings.append(w2v_model.wv[word])
#                 # print("Done")
#             else:
#                 sentence_embeddings.append([0.0]*w2v_model.vector_size)
#         embeddings.append(sentence_embeddings)
#     return embeddings

# get_sentence_embeddings(train_data, w2v_model)

def main(input_dir):
    # Set the hyperparameters
    hidden_size = 512
    num_classes = 2  # Positive and negative classes
    dropout_rate = 0.2
    learning_rate = 0.01
    num_epochs = 10
    batch_size = 1024
    weight_decay = 1e-5  # L2-norm regularization strength

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    w2v_model = Word2Vec.load(os.path.join(input_dir, 'word2vec.model'))
    
    train_data = get_sentence_embeddings(os.path.join(input_dir, 'train.csv'), w2v_model)
    test_data = get_sentence_embeddings(os.path.join(input_dir, 'test.csv'), w2v_model)
    val_data = get_sentence_embeddings(os.path.join(input_dir, 'val.csv'), w2v_model)

    train_labels = read_file(os.path.join(input_dir, 'train.labels.csv'))
    test_labels = read_file(os.path.join(input_dir, 'test.labels.csv'))
    val_labels = read_file(os.path.join(input_dir, 'val.labels.csv'))

    # train_data = read_file(os.path.join(input_dir, 'train_ns.csv'), False)
    # val_data = read_file(os.path.join(input_dir, 'val_ns.csv'), False)
    # test_data = read_file(os.path.join(input_dir, 'test_ns.csv'), False)
    # # train_labels = to_categorical(np.asarray(load_data(os.path.join(input_dir, 'train_ns.labels.csv'), True)))
    # # val_labels = to_categorical(np.asarray(load_data(os.path.join(input_dir, 'val_ns.labels.csv'), True)))
    # # test_labels = to_categorical(np.asarray(load_data(os.path.join(input_dir, 'test_ns.labels.csv'), True)))
    # train_labels = torch.tensor(read_file(os.path.join(input_dir, 'train_ns.labels.csv'), True)).type(torch.LongTensor)
    # val_labels = torch.tensor(read_file(os.path.join(input_dir, 'val_ns.labels.csv'), True)).type(torch.LongTensor)
    # test_labels = torch.tensor(read_file(os.path.join(input_dir, 'test_ns.labels.csv'), True)).type(torch.LongTensor)

    train_labels = train_labels.reshape(-1, num_classes)
    val_labels = val_labels.reshape(-1, num_classes)
    test_labels = test_labels.reshape(-1, num_classes)
    length = [len(s) for s in (train_data + test_data + val_data)]
    max_length = max(length)

    train_embeddings = get_sentence_embeddings(train_data, w2v_model)
    train_embeddings = pad_sequences(train_embeddings, maxlen=max_length, padding='post', truncating='post')
    val_embeddings = get_sentence_embeddings(val_data, w2v_model)
    val_embeddings = pad_sequences(val_embeddings, maxlen=max_length, padding='post', truncating='post')
    test_embeddings = get_sentence_embeddings(test_data, w2v_model)
    test_embeddings = pad_sequences(test_embeddings, maxlen=max_length, padding='post', truncating='post')

    train_embeddings = torch.tensor(train_embeddings)
    print("Train_embedding: ", len(train_embeddings))
    val_embeddings = torch.tensor(val_embeddings)
    test_embeddings = torch.tensor(test_embeddings)

    train_labels = torch.tensor(train_labels).type(torch.LongTensor)
    val_labels = torch.tensor(val_labels).type(torch.LongTensor)
    test_labels = torch.tensor(test_labels).type(torch.LongTensor)

    model = Classifier(w2v_model.vector_size, hidden_size, num_classes, dropout_rate)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9, weight_decay=weight_decay)

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0.0
        # print("model train !loop")
        for batch_idx in range(0, len(train_embeddings), batch_size):
            # print("model train loop inside")
            inputs = train_embeddings[batch_idx:batch_idx+batch_size].to(device)
            targets = train_labels[batch_idx:batch_idx+batch_size].to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            # print("Target Shape:", targets.shape)
            # print("Target Values:", targets)
            # print("Output Shape:", outputs.shape)
            # print("Output Values:", outputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

            # Print progress
            if (batch_idx + 1) % 10 == 1:
                print(f"Epoch [{epoch+1}/{num_epochs}], Batch [{batch_idx+1}/{len(train_embeddings)}], Loss: {loss.item():.4f}")

        avg_loss = total_loss / (len(train_embeddings) // batch_size + 1)

        # Validation
        model.eval()
        with torch.no_grad():
            val_inputs = val_embeddings.to(device)
            val_targets = val_labels.to(device)

            val_outputs = model(val_inputs)
            _, val_predicted = torch.max(val_outputs, dim=1)

            val_accuracy = accuracy_score(val_targets.cpu().numpy(), val_predicted.cpu().numpy())
            print(f"Epoch {epoch+1}/{num_epochs}: Avg Loss: {avg_loss:.4f} - Val Accuracy: {val_accuracy:.4f}")

    # Testing
    model.eval()
    with torch.no_grad():
        test_inputs = test_embeddings.to(device)
        test_targets = test_labels.to(device)

        test_outputs = model(test_inputs)
        _, test_predicted = torch.max(test_outputs, dim=1)

        test_accuracy = accuracy_score(test_targets.cpu().numpy(), test_predicted.cpu().numpy())
        print(f"Test Accuracy: {test_accuracy:.4f}")


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = ""
    if len(sys.argv) < 2:
        input_dir = input("Please provide the folder path: ")
    else:
        input_dir = sys.argv[1] + "/"
    main(input_dir)
