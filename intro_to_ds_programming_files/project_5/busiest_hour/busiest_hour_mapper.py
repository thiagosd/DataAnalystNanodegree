import sys
import string


def mapper():
    """
    In this exercise, for each turnstile unit, you will determine the date and time
    (in the span of this data set) at which the most people entered through the unit.

    The input to the mapper will be the final Subway-MTA dataset, the same as
    in the previous exercise. You can check out the csv and its structure below:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv

    For each line, the mapper should return the UNIT, ENTRIESn_hourly, DATEn, and
    TIMEn columns, separated by tabs. For example:
    'R001\t100000.0\t2011-05-01\t01:00:00'

    Since you are printing the output of your program, printing a debug
    statement will interfere with the operation of the grader. Instead,
    use the logging module, which we've configured to log to a file printed
    when you click "Test Run". For example:
    logging.info("My debugging message")
    """

    # write to csv file, that will be used by the reducer
    output_file = open("output.txt", "wb")

    text_file = open("turnstile_data_master_with_weather.csv", "r")
    rows = text_file.readlines()[1:]  # readlines and skip the header (1st line)
    for row in rows:
        data = row.strip().split(",")

        # csv file has 22 header columns
        # we only want rows with values in all header columns
        if len(data) != 22:
            continue

        # print key-value pair
        # index 1 = UNIT
        # index 2 = DATEn
        # index 3 = TIMEn
        # index 6 = ENTRIESn_hourly
        print "{0}\t{1}\t{2}\t{3}".format(data[1], data[6], data[2], data[3])
        output_file.write("{0}\t{1}\t{2}\t{3}".format(data[1], data[6], data[2], data[3]) + "\n")

mapper()