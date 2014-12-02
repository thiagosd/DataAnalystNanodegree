import pandas as pd
from ggplot import *


def plot_weather_data(turnstile_weather):
    ''' 
    plot_weather_data is passed a dataframe called turnstile_weather.
    Use turnstile_weather along with ggplot to make another data visualization
    focused on the MTA and weather data we used in Project 3.

    Make a type of visualization different than what you did in the previous exercise.
    Try to use the data in a different way (e.g., if you made a lineplot concerning
    ridership and time of day in exercise #1, maybe look at weather and try to make a
    histogram in this exercise). Or try to use multiple encodings in your graph if
    you didn't in the previous exercise.

    You should feel free to implement something that we discussed in class
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time-of-day or day-of-week
     * How ridership varies by subway station
     * Which stations have more exits or entries at different times of day

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/

    You can check out the link
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    to see all the columns and data points included in the turnstile_weather
    dataframe.

    However, due to the limitation of our Amazon EC2 server, we will give you only
    about 1/3 of the actual data in the turnstile_weather dataframe.
    '''

    #plot = ggplot(turnstile_weather, aes('EXITSn_hourly', 'ENTRIESn_hourly')) + stat_smooth(span=.15, color='black',
    #                                                                                        se=True) + geom_point(
    #    color='lightblue') + ggtitle("MTA Entries By The Hour!") + xlab('Exits') + ylab('Entries')
    #return plot

    # - Which stations have more exits or entries at different times of day
    turnstile_weather = turnstile_weather.copy()

    # create dataframe with sum of Entries
    hour_and_sumentries = turnstile_weather.groupby(['UNIT', 'Hour'], as_index=False).ENTRIESn_hourly.sum()
    hour_and_sumentries.rename(columns={'ENTRIESn_hourly': 'sum_ENTRIESn_hourly'}, inplace=True)

    # group by Hour, and get the index of rows with max Entries
    idx = hour_and_sumentries.groupby(['Hour'])['sum_ENTRIESn_hourly'].transform(max) == hour_and_sumentries[
        'sum_ENTRIESn_hourly']

    # create dataframe with max # of Entries
    hour_and_maxentries = hour_and_sumentries[idx == True]
    # reset index
    hour_and_maxentries.reset_index(inplace=True)
    # rename Entries column
    hour_and_maxentries = hour_and_maxentries.rename(columns={'sum_ENTRIESn_hourly': 'max_ENTRIESn_hourly'})

    plot2 = ggplot(hour_and_maxentries,
                   aes('Hour', 'max_ENTRIESn_hourly', color='UNIT')) + geom_point(size=30) + geom_line() + ggtitle(
        'Stations with more Entries by Hour') + xlab('Hour') + ylab('Max number of Entries') + scale_x_continuous(
        limits=(-1, 24), breaks=range(0, 24, 1)) + ylim(0, hour_and_maxentries['max_ENTRIESn_hourly'].max() + 10000)
    return plot2


if __name__ == "__main__":
    image = "plot.png"
    # with open(image, "wb") as f:
    turnstile_weather = pd.read_csv("turnstile_data_master_with_weather.csv")
    turnstile_weather['datetime'] = turnstile_weather['DATEn'] + ' ' + turnstile_weather['TIMEn']
    gg = plot_weather_data(turnstile_weather)
    #ggsave(f, gg)
    ggsave(image, gg, width=11, height=8)