import pandas as pd
from ggplot import *


def plot_weather_data(turnstile_weather):
    '''
    You are passed in a dataframe called turnstile_weather. 
    Use turnstile_weather along with ggplot to make a data visualization
    focused on the MTA and weather data we used in assignment #3.  
    You should feel free to implement something that we discussed in class 
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.  

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time of day or day of week
     * How ridership varies based on Subway station
     * Which stations have more exits or entries at different times of day

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/
     
    You can check out:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
     
    To see all the columns and data points included in the turnstile_weather 
    dataframe. 
     
    However, due to the limitation of our Amazon EC2 server, we are giving you about 1/3
    of the actual data in the turnstile_weather dataframe
    '''

    # - Ridership by time of day or day of week

    # plot = ggplot(turnstile_weather, aes('Hour', 'ENTRIESn_hourly')) + geom_bar(stat='bar', color='green') + ggtitle(
    # '# of Entries by Hour') + xlab('Hour') + ylab('# of Entries')

    # return plot


    # - Ridership by day of week

    turnstile_weather = turnstile_weather.copy()
    # add day of week to the dataframe
    turnstile_weather['weekday'] = pd.DatetimeIndex(turnstile_weather['DATEn']).weekday

    weekday_and_averageentries = turnstile_weather.groupby('weekday', as_index=False).ENTRIESn_hourly.mean()
    weekday_and_averageentries.rename(columns={'ENTRIESn_hourly': 'avg_ENTRIESn_hourly'}, inplace=True)

    plot2 = ggplot(weekday_and_averageentries, aes('weekday', 'avg_ENTRIESn_hourly')) + geom_bar(stat='bar',
                                                                                                 color='yellow') + ggtitle(
        'avg # of Entries by Day of Week') + xlab('Day of Week') + ylab('avg # of Entries') + scale_x_discrete(
        limits=(-1, 7), breaks=range(0, 7, 1), labels=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    return plot2


if __name__ == "__main__":
    image = "plot.png"
    # with open(image, "wb") as f:
    turnstile_weather = pd.read_csv("turnstile_data_master_with_weather.csv")
    turnstile_weather['datetime'] = turnstile_weather['DATEn'] + ' ' + turnstile_weather['TIMEn']
    gg = plot_weather_data(turnstile_weather)
    # ggsave(f, gg)
    ggsave(image, gg, width=11, height=8)



# http://stackoverflow.com/questions/15705630/python-how-can-i-get-the-row-which-has-the-max-value-in-goups-making-groupby