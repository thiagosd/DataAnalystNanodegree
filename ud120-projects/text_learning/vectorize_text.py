#!/usr/bin/python

import pickle
import sys
import re
import os
# import nltk
#from nltk.corpus import stopwords


sys.path.append("../tools/")
from parse_out_email_text import parseOutText

"""
    starter code to process the emails from Sara and Chris to extract
    the features and get the documents ready for classification

    the list of all the emails from Sara are in the from_sara list
    likewise for emails from Chris (from_chris)

    the actual documents are in the Enron email dataset, which
    you downloaded/unpacked in Part 0 of the first mini-project

    the data is stored in lists and packed away in pickle files at the end

"""

#sw = stopwords.words("english")

from_sara = open("from_sara.txt", "r")
from_chris = open("from_chris.txt", "r")

from_data = []
word_data = []

### temp_counter is a way to speed up the development--there are
### thousands of emails from Sara and Chris, so running over all of them
### can take a long time
### temp_counter helps you only look at the first 200 emails in the list
temp_counter = 0

for name, from_person in [("sara", from_sara), ("chris", from_chris)]:
    for path in from_person:
        ### only look at first 200 emails when developing
        ### once everything is working, remove this line to run over full dataset
        temp_counter += 1
        #if temp_counter < 200:

        #path = os.path.join('..', 'tools', path[:-1])
        path = os.path.join('..', path[:-1])
        email = open(path, "r")

        ### use parseOutText to extract the text from the opened email
        parsed_email = parseOutText(email)

        ### use str.replace() to remove any instances of the words
        ### ["sara", "shackleton", "chris", "germani"]
        parsed_email = parsed_email.replace("sara", "").replace("shackleton", "").replace("chris", "").replace(
            "germani", "").replace("sshacklensf", "").replace("cgermannsf", "")
        ### append the text to word_data
        word_data.append(parsed_email)
        ### append a 0 to from_data if email is from Sara, and 1 if email is from Chris
        if name == 'sara':
            from_data.append(0)
        elif name == 'chris':
            from_data.append(1)

        email.close()
#print word_data[152]
print "emails processed"
from_sara.close()
from_chris.close()

pickle.dump(word_data, open("your_word_data.pkl", "w"))
pickle.dump(from_data, open("your_email_authors.pkl", "w"))

### in Part 4, do TfIdf vectorization here
from sklearn.feature_extraction.text import TfidfVectorizer
#rom nltk.corpus import stopwords

#sw = stopwords.words("english")

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(word_data)
idf = vectorizer._tfidf.idf_
print idf
vocab_list = vectorizer.get_feature_names()
#print dict(zip(vectorizer.get_feature_names(), idf))

