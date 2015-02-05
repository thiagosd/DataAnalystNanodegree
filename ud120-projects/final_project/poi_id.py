#!/usr/bin/python

import sys
import pickle
import math
import matplotlib.pyplot
#from tester import test_classifier, dump_classifier_and_data
from multi_tester import test_classifier, dump_classifier_and_data
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.decomposition import PCA
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

# end helper functions


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'salary', 'bonus']
#, 'total_payments', 'expenses', 'total_stock_value', 'from_oi_to_this_person', 'from_this_person_to_poi'

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

# clf = GaussianNB()
scaler = StandardScaler()
min_max_scaler = MinMaxScaler()

pca = PCA(copy=True, n_components=5, whiten=False)

clf_gaussian = GaussianNB()
clf_svc = SVC(random_state=None)  # very slow
clf_tree = DecisionTreeClassifier()
clf_ada = AdaBoostClassifier()
clf_forest = RandomForestClassifier()

estimator_gauss = [('scaler', scaler), ('reduce_dim', pca), ('gauss', clf_gaussian)]
estimator_tree = [('scaler', scaler), ('reduce_dim', pca), ('tree', clf_tree)]
estimator_ada = [('scaler', scaler), ('reduce_dim', pca), ('ada', clf_ada)]
estimator_svc = [('scaler', scaler), ('reduce_dim', pca), ('svc', clf_svc)]
estimator_forest = [('scaler', scaler), ('reduce_dim', pca), ('forest', clf_forest)]

clf_gaussian = Pipeline(estimator_gauss)
clf_tree = Pipeline(estimator_tree)
clf_ada = Pipeline(estimator_ada)
clf_svc = Pipeline(estimator_svc)
clf_forest = Pipeline(estimator_forest)

### Task 5: Tune your classifier to achieve better than .3 precision and recall

params = dict(reduce_dim__n_components=[1, 2], tree__random_state=[0, 1, 2, 3],
              tree__min_samples_split=[2, 3, 4, 10], )
clf_tree = GridSearchCV(clf_tree, param_grid=params, n_jobs=-1)

params = dict(reduce_dim__n_components=[1, 2], ada__n_estimators=[10, 25, 50, 75, 100],
              ada__algorithm=['SAMME', 'SAMME.R'])
clf_ada = GridSearchCV(clf_ada, param_grid=params, n_jobs=-1)

params = dict(reduce_dim__n_components=[1, 2], svc__kernel=['linear', 'rbf'], svc__C=[1, 10, 100, 1e3, 5e3],
              svc__gamma=[0.0, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1])
clf_svc = GridSearchCV(clf_svc, param_grid=params, n_jobs=-1)

params = dict(reduce_dim__n_components=[1, 2], forest__n_estimators=[1, 10, 50, 100, 1000],
              forest__random_state=[None, 1, 2, 5, 10])
clf_forest = GridSearchCV(clf_forest, param_grid=params, n_jobs=-1)


### using our testing script.
### Because of the small size of the dataset, the script uses stratified
### shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
if __name__ == '__main__':
    i = 0
    for clf in [clf_forest, clf_tree, clf_ada, clf_svc]:
        #test_classifier(clf, my_dataset, features_list)

        ### Dump your classifier, dataset, and features_list so
        ### anyone can run/check your results.
        dump_classifier_and_data(clf, my_dataset, features_list, i)
        i += 1