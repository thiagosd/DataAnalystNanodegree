import numpy
import pandas

def normalize_features(array):
    """
    Normalize the features in our data set.
    """
    array_normalized = (array - array.mean())/array.std()
    mu = array.mean()
    sigma = array.std()

    return array_normalized, mu, sigma


def compute_cost(features, values, theta):
    """
    Compute the cost function given a set of features / values, and values for our thetas.
    """
    m = len(values)
    sum_of_square_errors = numpy.square(numpy.dot(features, theta) - values).sum()
    cost = sum_of_square_errors / (2*m)

    return cost


def gradient_descent(features, values, theta, alpha, num_iterations):
    """
    Perform gradient descent given a data set with an arbitrary number of features.
    """

    # Write some code here that updates the values of theta a number of times equal to
    # num_iterations.  Every time you have computed the cost for a given set of thetas,
    # you should append it to cost_history.  The function should return both the final
    # values of theta and the cost history.

    cost_history = []
    m = len(values)
    for i in range(num_iterations):
        # hypothesis/prediction = vector of theta_n x features_n
        hypothesis = numpy.dot(features, theta)

        # alpha divided by m, times vector of values - hypothesis x features, plus theta.
        theta += (alpha / m) * numpy.dot(values - hypothesis, features)
        #numpy.append(theta, theta_i)
        # calculate cost and append to cost_history
        cost_history.append(compute_cost(features, values, theta))


    return theta, pandas.Series(cost_history)  # leave this line for the grader


if __name__ == '__main__':

    # Read data into a pandas dataframe.
    data = pandas.read_csv('baseball_stats_regression.csv')

    # Isolate features / values.
    features = data[['height', 'weight']]
    values = data[['HR']]
    m = len(values)

    # Normalize features.
    features, mu, sigma = normalize_features(features)

    # Add a column of ones to features for constant term.
    features['ones'] = numpy.ones(m)
    features_array = numpy.array(features[['ones', 'height', 'weight']])
    values_array = numpy.array(values).flatten()

    # Set values for alpha, number of iterations.
    alpha = 0.01
    num_iterations = 1000

    # Initialize theta and perform gradient descent.
    theta_gradient_descent = numpy.zeros(3)
    theta_gradient_descent, cost_history = gradient_descent(features_array, values_array, theta_gradient_descent,
                                                            alpha, num_iterations)

    print "Theta =\n{theta}\n\nCost History = \n{history}".format(theta=theta_gradient_descent, history=cost_history)




#http://docs.scipy.org/doc/numpy/reference/generated/numpy.append.html
#http://aimotion.blogspot.com/2011/10/machine-learning-with-python-linear.html
#http://stackoverflow.com/questions/17784587/gradient-descent-using-python-and-numpy
#http://www.bogotobogo.com/python/python_numpy_batch_gradient_descent_algorithm.php

