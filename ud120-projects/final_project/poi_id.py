#!/usr/bin/python

import matplotlib.pyplot as plt
import sys
import pickle
import matplotlib
import numpy as np

sys.path.append("../tools/")

from feature_format import featureFormat
from feature_format import targetFeatureSplit

# begin helper functions
def plotSalaryBonus(data_dict):
    """
        plot Salary and Bonus
    """
    for point in data_dict:
        salary = data_dict[point]['salary']
        bonus = data_dict[point]['bonus']
        matplotlib.pyplot.scatter(salary, bonus)

    matplotlib.pyplot.xlabel("salary")
    matplotlib.pyplot.ylabel("bonus")
    matplotlib.pyplot.show()

# end helper functions

### features_list is a list of strings, each of which is a feature name
### first feature must be "poi", as this will be singled out as the label
features_list = ['poi', 'salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus',
                 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses',
                 'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees',
                 'to_messages', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi',
                 'shared_receipt_with_poi']



### load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r"))

### we suggest removing any outliers before proceeding further
# scatterplot bonus and salary to visually identify outliers
plotSalaryBonus(data_dict)

# clearly there is an outlier, remove it
data_dict.pop('TOTAL', 0)
# check for outliers again. There are a few people with high salary or bonus, but we want to keep them because they are potential POI
plotSalaryBonus(data_dict)

### if you are creating any new features, you might want to do that here
### store to my_dataset for easy export below
my_dataset = data_dict


### these two lines extract the features specified in features_list
### and extract them from data_dict, returning a numpy array
data = featureFormat(my_dataset, features_list)

### if you are creating new features, could also do that here



### split into labels and features (this line assumes that the first
### feature in the array is the label, which is why "poi" must always
### be first in features_list
labels, features = targetFeatureSplit(data)


### machine learning goes here!
### please name your classifier clf for easy export below
from sklearn import tree
clf = None


### dump your classifier, dataset and features_list so 
### anyone can run/check your results
pickle.dump(clf, open("my_classifier.pkl", "w"))
pickle.dump(data_dict, open("my_dataset.pkl", "w"))
pickle.dump(features_list, open("my_feature_list.pkl", "w"))