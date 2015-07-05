#!/usr/bin/python

import sys
import pickle

import matplotlib.pyplot

# from multi_tester import test_classifier, dump_classifier_and_data
# from sklearn.grid_search import GridSearchCV
from tester import test_classifier, dump_classifier_and_data
from sklearn.pipeline import Pipeline
from sklearn.decomposition import RandomizedPCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler

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
        matplotlib.pyplot.scatter(salary, bonus, c='red' if data_dict[point]['poi'] else 'green', s=40)
        if point == 'TOTAL':
            matplotlib.pyplot.annotate('"Total" Outlier', xy=(salary, bonus), xytext=(-20, 20),
                                       textcoords='offset points', ha='right', va='bottom',
                                       bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                                       arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    matplotlib.pyplot.xlabel("Salary")
    matplotlib.pyplot.ylabel("Bonus")
    # matplotlib.pyplot.scatter(0, 0, c='red', s=40, label='POI')
    # matplotlib.pyplot.scatter(0, 0, c='green', s=40, label='Non-POI')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.show()


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
features_list = ['poi', 'bonus', 'expenses']

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
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
scaler = StandardScaler()

pca = RandomizedPCA(copy=True, whiten=False, n_components=2)

clf = DecisionTreeClassifier(random_state=10, min_samples_split=2)

estimator_tree = [('scaler', scaler), ('reduce_dim', pca), ('tree', clf)]

clf = Pipeline(estimator_tree)


### Task 5: Tune your classifier to achieve better than .3 precision and recall

# params = dict(reduce_dim__n_components=[1, 2, 3], tree__random_state=[None, 0, 1, 2, 10, 20, 40, 100, 1000],
#              tree__min_samples_split=[2, 4, 6])
# clf_tree = GridSearchCV(clf_tree, param_grid=params, n_jobs=-1, scoring='recall')

### using our testing script.
### Because of the small size of the dataset, the script uses stratified
### shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
test_classifier(clf, my_dataset, features_list)

### Dump your classifier, dataset, and features_list so
### anyone can run/check your results.
dump_classifier_and_data(clf, my_dataset, features_list)
