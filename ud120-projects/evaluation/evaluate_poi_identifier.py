#!/usr/bin/python
from __future__ import division

"""
    starter code for the evaluation mini-project
    start by copying your trained/tested POI identifier from
    that you built in the validation mini-project

    the second step toward building your POI identifier!

    start by loading/formatting the data

"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

### add more features to features_list!
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)

### your code goes here
from sklearn import tree
from sklearn import cross_validation
from sklearn.metrics import accuracy_score, precision_score, recall_score

features_train, features_test, label_train, label_test = cross_validation.train_test_split(features, labels,
                                                                                           test_size=0.3,
                                                                                           random_state=42)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(features_train, label_train)
#print clf.score(features_test, label_test)
preds = clf.predict(features_test)


#Number of POIs in Test Set
poi_list = [pred for pred in preds if pred == 1.0]
print len(poi_list)

#Number of People in Test Set
print len(label_test)

#Accuracy of Biased Identifier
biased_identifier = [0 for item in label_test]
accuracy = accuracy_score(label_test, biased_identifier)
print accuracy

#Number of True Positives
print len([label for label, pred in zip(label_test, preds) if pred == label == 1.0])

#Unpacking Into Precision and Recall
print precision_score(label_test, preds)

#Recall of Your POI Identifier
print recall_score(label_test, preds)

#How Many True Positives?
predictions = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1]
true_labels = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]
print len([label for label, pred in zip(true_labels, predictions) if pred == label == 1.0])

#How Many True Negatives?
predictions = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1]
true_labels = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]
print len([label for label, pred in zip(true_labels, predictions) if pred == label == 0.0])

#False Positives?
predictions = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1]
true_labels = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]
print len([label for label, pred in zip(true_labels, predictions) if pred == 1.0 and label == 0.0])


#False Negatives?
predictions = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1]
true_labels = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]
print len([label for label, pred in zip(true_labels, predictions) if pred == 0.0 and label == 1.0])

#Precision
predictions = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1]
true_labels = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]
true_positive = len([label for label, pred in zip(true_labels, predictions) if pred == label == 1.0])
false_positive = len([label for label, pred in zip(true_labels, predictions) if pred == 1.0 and label == 0.0])

precision = true_positive / (true_positive + false_positive)
print precision

#Recall
false_negative = len([label for label, pred in zip(true_labels, predictions) if pred == 0.0 and label == 1.0])
recall = true_positive / (true_positive + false_negative)
print recall





