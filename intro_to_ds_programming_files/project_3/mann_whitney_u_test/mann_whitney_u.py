import numpy as np
import scipy
import scipy.stats
import pandas as pd


def mann_whitney_plus_means(turnstile_weather):
    '''
    This function will consume the turnstile_weather dataframe containing our final turnstile-Subway data. This 
    function should return the mean number of entries with rain, the mean number of entries without rain, and the
    Mann-Whitney U statistic and p-value.  You should feel free to use scipy's Mann-Whitney implementation, and also
    might find it useful to use numpy's mean function.  Here's some documentation on that:

    http://docs.scipy.org/doc/numpy/reference/generated/numpy.mean.html
    '''

    df_rain = turnstile_weather[turnstile_weather['rain'] == 1]
    df_notrain = turnstile_weather[turnstile_weather['rain'] == 0]

    with_rain_mean = np.mean(df_rain['ENTRIESn_hourly'])
    without_rain_mean = np.mean(df_notrain['ENTRIESn_hourly'])

    U, p = scipy.stats.mannwhitneyu(df_rain['ENTRIESn_hourly'], df_notrain['ENTRIESn_hourly'])

    return with_rain_mean, without_rain_mean, U, p

if __name__ == "__main__":
    input_filename = "turnstile_data_master_with_weather.csv"
    turnstile_master = pd.read_csv(input_filename)
    student_output = mann_whitney_plus_means(turnstile_master)

    print student_output


# links used for Project 3 - (Task: 4 - Ridership on Rainy vs. Nonrainy Days)
#https://explorable.com/mann-whitney-u-test
#http://graphpad.com/guides/prism/6/statistics/index.htm?how_the_mann-whitney_test_works.htm