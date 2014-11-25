import numpy as np
import pandas as pd
import scipy
import statsmodels
import statsmodels.api as sm


def normalize_features(array):
   """
   Normalize the features in our data set.
   """
   array_normalized = (array-array.mean())/array.std()
   mu = array.mean()
   sigma = array.std()

   return array_normalized, mu, sigma


"""
In this optional exercise, you should complete the function called
predictions(turnstile_weather). This function takes in our pandas
turnstile weather dataframe, and returns a set of predicted ridership values,
based on the other information in the dataframe.

You should attempt to implement another type of linear regression,
that you may have read about, such as ordinary least squares regression:
http://en.wikipedia.org/wiki/Ordinary_least_squares

This is your playground. Go wild!

How does your choice of linear regression compare to linear regression
with gradient descent?

You can look at the information contained in the turnstile_weather dataframe below:
https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv

Note: due to the memory and CPU limitation of our amazon EC2 instance, we will
give you a random subset (~15%) of the data contained in turnstile_data_master_with_weather.csv

If you receive a "server has encountered an error" message, that means you are hitting
the 30 second limit that's placed on running your program. See if you can optimize your code so it
runs faster.
"""

def predictions(weather_turnstile):
    #
    # Your implementation goes here. Feel free to write additional
    # helper functions
    #

    #weather_turnstile.dropna(inplace=True)
    weather_turnstile = weather_turnstile.dropna()

    dummy_units = pd.get_dummies(weather_turnstile['UNIT'], prefix='unit')
    features = weather_turnstile[['rain', 'precipi', 'Hour', 'meantempi']].join(dummy_units)
    values = weather_turnstile[['ENTRIESn_hourly']]
    m = len(values)

    # normalize features
    features, mu, sigma = normalize_features(features)
    features['ones'] = np.ones(m) # add column to interception
    #print features
    model = sm.OLS(values, features)
    results = model.fit()
    #prediction = np.dot(features, results.params)
    prediction = results.predict()

    return prediction

def compute_r_squared(data, predictions):
    SST = ((data-np.mean(data))**2).sum()
    SSReg = ((predictions-np.mean(data))**2).sum()
    r_squared = SSReg / SST

    return r_squared

if __name__ == "__main__":
    input_filename = "turnstile_data_master_with_weather_smaller.csv"
    turnstile_master = pd.read_csv(input_filename, low_memory=False)
    predicted_values = predictions(turnstile_master)
    r_squared = compute_r_squared(turnstile_master['ENTRIESn_hourly'], predicted_values)

    print r_squared


#http://stackoverflow.com/questions/21827594/raise-linalgerrorsvd-did-not-converge-linalgerror-svd-did-not-converge-in-m
#http://pandas.pydata.org/pandas-docs/dev/generated/pandas.DataFrame.dropna.html
#http://stackoverflow.com/questions/13218461/predicting-values-using-an-ols-model-with-statsmodels
#https://github.com/statsmodels/statsmodels/blob/master/examples/python/ols.py