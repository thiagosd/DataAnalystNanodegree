#!/usr/bin/python

import sys
import pickle
import math
import matplotlib.pyplot
# from tester import test_classifier, dump_classifier_and_data
#from multi_tester import test_classifier, dump_classifier_and_data
from tester import test_classifier, dump_classifier_and_data
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
#from sklearn.decomposition import PCA
from sklearn.decomposition import RandomizedPCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler

sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit


# begin helper functions
def plt_salary_bonus(data_dict):
    """
        plot Salary and Bonus
    """
    for point in data_dict:
        salary = data_dict[point]['salary']
        bonus = data_dict[point]['bonus']
        matplotlib.pyplot.scatter(salary, bonus)

    matplotlib.pyplot.xlabel("salary")
    matplotlib.pyplot.ylabel("bonus")
    # matplotlib.pyplot.show()


def computeFraction(poi_messages, all_messages):
    """ given a number messages to/from POI (numerator)
        and number of all messages to/from a person (denominator),
        return the fraction of messages to/from that person
        that are from/to a POI
   """
    if poi_messages == 'NaN' or all_messages == 'NaN' or poi_messages == 0 or all_messages == 0:
        fraction = 0.
    else:
        fraction = float(poi_messages) / float(all_messages)

    return fraction

# end helper functions


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'bonus', 'total_payments', 'expenses', 'fraction_to_poi']
'''
1st
['poi', 'salary', 'bonus', 'total_payments', 'expenses', 'from_poi_to_this_person', 'from_this_person_to_poi', 'fraction_from_poi', 'fraction_to_poi', 'fraction_bonus_to_salary']
#[ 0.01889231  0.1721201   0.26686628  0.31702631  0.          0.05422794  0.10243056  0.0684365   0.        ]
#from_poi_to_this_person, fraction_bonus_to_salary

2nd
[ 0.09828486  0.22634804  0.18747374  0.26882369  0.05422794  0.09640523  0.0684365 ]
[ 0.0808671   0.28057598  0.26686628  0.25505152  0.          0.04820261  0.0684365 ]
from_this_person_to_poi

[ 0.06709493  0.22634804  0.26686628  0.26882369  0.04820261  0.12266444]
salary, fraction_from_poi
'''

### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r"))

### Task 2: Remove outliers
# scatterplot bonus and salary to visually identify outliers
plt_salary_bonus(data_dict)

# clearly there is an outlier, remove it
data_dict.pop('TOTAL', 0)
# check for outliers again.
# There are a few people with high salary or bonus, but we want to keep them because they are potential POI
plt_salary_bonus(data_dict)

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = data_dict

for name in my_dataset:
    data_point = my_dataset[name]

    fraction_from_poi = computeFraction(data_point["from_poi_to_this_person"], data_point["to_messages"])
    data_point["fraction_from_poi"] = fraction_from_poi

    fraction_to_poi = computeFraction(data_point["from_this_person_to_poi"], data_point["to_messages"])
    data_point["fraction_to_poi"] = fraction_to_poi

    fraction_bonus_to_salary = computeFraction(data_point["salary"], data_point["bonus"])
    data_point["fraction_bonus_to_salary"] = fraction_to_poi



### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list)
#data = data[:len(data)*0.1]

labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# clf = GaussianNB()
scaler = StandardScaler()
min_max_scaler = MinMaxScaler()

#pca = PCA(copy=True, whiten=False)
pca = RandomizedPCA(copy=True, whiten=False, n_components=6)

clf_gaussian = GaussianNB()
clf_tree = DecisionTreeClassifier(min_samples_split=2)
clf_ada = AdaBoostClassifier()
clf_forest = RandomForestClassifier()

estimator_gauss = [('scaler', scaler), ('reduce_dim', pca), ('gauss', clf_gaussian)]
estimator_tree = [('scaler', scaler), ('tree', clf_tree)]


clf_gaussian = Pipeline(estimator_gauss)
clf_tree = Pipeline(estimator_tree)

### Task 5: Tune your classifier to achieve better than .3 precision and recall

params = dict(reduce_dim__n_components=[None, 0, 2, 4], tree__random_state=[None, 0, 1, 2, 10, 20, 40])
#clf_tree = GridSearchCV(clf_tree, param_grid=params, scoring='recall')


### using our testing script.
### Because of the small size of the dataset, the script uses stratified
### shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
if __name__ == '__main__':
    #test_classifier(clf_tree, my_dataset, features_list)

    ### Dump your classifier, dataset, and features_list so
    ### anyone can run/check your results.
    dump_classifier_and_data(clf_tree, my_dataset, features_list)