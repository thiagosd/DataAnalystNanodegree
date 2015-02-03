#!/usr/bin/python

import sys
import pickle
import matplotlib.pyplot


sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data

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
    matplotlib.pyplot.show()


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'salary', 'bonus', 'total_payments', 'expenses']

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

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.grid_search import GridSearchCV

#clf = GaussianNB()
clf_gaussian = GaussianNB()
clf_scv = SVC(kernel='linear', C=1.0, random_state=None) #very slow
pca = PCA(copy=True, n_components=None, whiten=False)
clf_tree = DecisionTreeClassifier(random_state=1, min_samples_split=2)
#clf_ada = AdaBoostClassifier(n_estimators=25, algorithm='SAMME')

estimators = [('reduce_dim', pca), ('tree', clf_tree), ('gauss', clf_gaussian)]
clf = Pipeline(estimators)


### Task 5: Tune your classifier to achieve better than .3 precision and recall

#params = dict(reduce_dim__n_components=[2, 5, 10])
#grid_search = GridSearchCV(clf, param_grid=params)

### using our testing script.
### Because of the small size of the dataset, the script uses stratified
### shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

test_classifier(clf, my_dataset, features_list)

### Dump your classifier, dataset, and features_list so
### anyone can run/check your results.

dump_classifier_and_data(clf, my_dataset, features_list)