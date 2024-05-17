# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:00:18 2024

@author: 15485
"""

import random
import csv
import sys
def main():
    neg_wostopwords, neg_wistopwords = dataperp(negative,0)
    pos_wostopwords, pos_wistopwords = dataperp(positive,1)
    corpus_wostopword = neg_wostopwords+pos_wostopwords
    corpus_wistopword = neg_wistopwords+pos_wistopwords
    test_train_val_split(corpus_wostopword, 1)
    test_train_val_split(corpus_wistopword, 0)
    pass

def dataperp(str,indicator):
    file_sample = open(str, "r").read().lower()
    #print(type(file_sample))
    characters = ['!','"','#','$','%','&','(',')','*','+','/',':',';','<','=','>','@','^','`','|','~','\t','[',']','{','}','\\']
    for i in characters:
        file_sample=file_sample.replace(i,"") 
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 
                 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', 
                 "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 
                 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 
                 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
                 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 
                 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 
                 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 
                 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 
                 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 
                 "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', 
                 "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 
                 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    lst1 = file_sample.splitlines()
    lst2 = []
    lst3 = []    
    for i in lst1:
        lst2.append(i.split())  
    for i in lst2:
        lst_temp = []
        for j in i:            
            if j not in stopwords:                    
                    lst_temp.append(j)
        lst3.append(lst_temp)    

    lst_sw = []
    lst_ns = []
    if indicator == 1:
        for i in lst2:
            pos_sw = [i,1]
            lst_sw.append(pos_sw)
        for i in lst3:
            pos_ns = [i,1]
            lst_ns.append(pos_ns)       
    if indicator == 0:
        for i in lst2:
            neg_sw = [i,0]
            lst_sw.append(neg_sw)
        for i in lst3:
            neg_ns = [i,0]
            lst_ns.append(neg_ns)  
    return lst_ns,lst_sw

def test_train_val_split(data, indicator):
    data1=data
    random.shuffle(data)
    size = len(data)
    train_data = data[:int(size*0.8)]
    data = data[int(size*0.8):]
    random.shuffle(data)
    test_data =  data[:int(size*0.1)]
    data = data[int(size*0.1):]
    random.shuffle(data)
    valid_data = data[:int(size*0.1)]
    if(indicator==1):
        csv_create_wostopwords(data1, train_data, valid_data, test_data)
    if(indicator==0):
        csv_create_wistopwords(data1, train_data, valid_data, test_data)

def csv_create_wostopwords(lst1, lst2, lst3, lst4):
    main_lst1 = []
    labels_lst1 = []
    for i in lst1:
        main_lst1.append(i[0])
        labels_lst1.append([i[1]])
    with open(location + 'out_ns.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(main_lst1)
    with open(location + 'out_ns.labels.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(labels_lst1)        
    main_lst1 = []
    labels_lst1 = []
    for i in lst2:
        main_lst1.append(i[0])
        labels_lst1.append([i[1]])
    with open(location + 'train_ns.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(main_lst1)
    with open(location + 'train_ns.labels.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(labels_lst1)
    main_lst1 = []
    labels_lst1 = []
    for i in lst3:
        main_lst1.append(i[0])
        labels_lst1.append([i[1]])
    with open(location + 'val_ns.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(main_lst1)
    with open(location + 'val_ns.labels.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(labels_lst1)        
    main_lst1 = []
    labels_lst1 = []
    for i in lst4:
        main_lst1.append(i[0])
        labels_lst1.append([i[1]])
    with open(location + 'test_ns.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(main_lst1)
    with open(location + 'test_ns.labels.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(labels_lst1)        

def csv_create_wistopwords(lst1, lst2, lst3, lst4):
    main_lst1 = []
    labels_lst1 = []
    for i in lst1:
        main_lst1.append(i[0])
        labels_lst1.append([i[1]])
    with open(location + 'out.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(main_lst1)
    with open(location + 'out.labels.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(labels_lst1)  
    main_lst1 = []
    labels_lst1 = []
    for i in lst2:
        main_lst1.append(i[0])
        labels_lst1.append([i[1]])
    with open(location + 'train.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(main_lst1)
    with open(location + 'train.labels.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(labels_lst1)  
    main_lst1 = []
    labels_lst1 = []
    for i in lst3:
        main_lst1.append(i[0])
        labels_lst1.append([i[1]])
    with open(location + 'val.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(main_lst1)
    with open(location + 'val.labels.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(labels_lst1)
    main_lst1 = []
    labels_lst1 = []
    for i in lst4:
        main_lst1.append(i[0])
        labels_lst1.append([i[1]])
    with open(location + 'test.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(main_lst1) 
    with open(location + 'test.labels.csv', 'w', newline='') as func:
        write = csv.writer(func)
        write.writerows(labels_lst1)               
                       

if __name__ == "__main__":
    if len(sys.argv) == 2:
        positive = sys.argv[1] + "//pos.txt"
        negative = sys.argv[1] + "//neg.txt"
        location = sys.argv[1] + "/"
    else:
        print("Error in command line arguments, use 'python a1/main.py [arg]' format for running the code.")
    main()