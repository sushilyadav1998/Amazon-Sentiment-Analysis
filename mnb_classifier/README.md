######  Note: I had made certain modifications in the a1 code to save the labels txt files. I have copied the updated files in the data directory. Please consider the labels and data from the a2/data directory.
To run the file use following command: 
python main.py data
python inference.py data/sentence_test.txt mnb_bi_ns

### Classification Accuracies after Multinomial Naïve Bayes (MNB) classifier to classify the documents in the Amazon corpus into positive and negative classes.

| Stopwords removed | Text features    | Accuracy (test set) |
|-------------------|------------------|---------------------|
| Yes (without stopword)              | Unigrams         |        80.76%            |
| Yes (without stopword)            | Bigrams          |     79.41625%                |
| Yes (without stopword)              | Unigrams + Bigrams |       82.56375%            |
| No (with stopword)               | Unigrams         |    80.9375%                 |
| No (with stopword)                | Bigrams          |       82.7325%              |
| No (with stopword)                | Unigrams + Bigrams |        83.50875%             |

## Short Report
##### Question a: Which condition performed better: with or without stopwords? Write a brief paragraph (5-6 sentences) discussing why you think there is a difference in performance.

##### Answer: 
From the accuracy table, it is evident that the text with stopwords exhibits slightly higher accuracy compared to the text without stopwords. This could be attributed to the idea that stopwords potentially contribute meaningful information to the overall sentence. However, upon closer inspection, the difference in accuracies between the two conditions is minimal. Additionally, the choice of stopwords can significantly influence the model's performance. Personally, I would opt to train the model without stopwords, as it reduces computational time and enables the model to learn more sophisticated representations of the text. It is crucial to select the list of stopwords carefully, considering that certain stopwords, like "not," can completely alter the meaning of a sentence. for example "I am not happy", the word 'not' completely changes the meaning of a sentence and if 'not' is used in the stopwords list for classifying the corpus into positive and negative feedback, then the model would not perform well if trained on the without stopword corpus. 

##### Question b: Which condition performed better: unigrams, bigrams or unigrams+bigrams? Briefly (in 5-6 sentences) discuss why you think there is a difference?

##### Answer: 
The combination of unigram and bigram performed better in classifiying the text corpus into positive and negative classes. this is because if we just consider the unigrams to train the model, then the model would not learn the complete context of the sentence. Based on the accuracy table, the condition of "No (with stopword) Unigrams + Bigrams" achieved the highest accuracy at 83.50875%. This suggests that combining both unigrams and bigrams as text features leads to improved performance. By incorporating both individual words (unigrams) and pairs of consecutive words (bigrams), the model gains a more comprehensive understanding of the text, capturing both local and global context. Unigrams alone may overlook important contextual cues, while bigrams alone may lack the granularity of individual words. The combination of unigrams and bigrams allows for a more nuanced representation of the text, enabling the model to capture both micro and macro-level language patterns, ultimately resulting in higher accuracy.