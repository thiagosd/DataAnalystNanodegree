import sys
import time


def reducer():
    '''
    Write a reducer that will compute the busiest date and time (that is, the
    date and time with the most entries) for each turnstile unit. Ties should
    be broken in favor of datetimes that are later on in the month of May. You
    may assume that the contents of the reducer will be sorted so that all entries
    corresponding to a given UNIT will be grouped together.

    The reducer should print its output with the UNIT name, the datetime (which
    is the DATEn followed by the TIMEn column, separated by a single space), and
    the number of entries at this datetime, separated by tabs.

    For example, the output of the reducer should look like this:
    R001    2011-05-11 17:00:00	   31213.0
    R002	2011-05-12 21:00:00	   4295.0
    R003	2011-05-05 12:00:00	   995.0
    R004	2011-05-12 12:00:00	   2318.0
    R005	2011-05-10 12:00:00	   2705.0
    R006	2011-05-25 12:00:00	   2784.0
    R007	2011-05-10 12:00:00	   1763.0
    R008	2011-05-12 12:00:00	   1724.0
    R009	2011-05-05 12:00:00	   1230.0
    R010	2011-05-09 18:00:00	   30916.0
    ...
    ...

    Since you are printing the output of your program, printing a debug
    statement will interfere with the operation of the grader. Instead,
    use the logging module, which we've configured to log to a file printed
    when you click "Test Run". For example:
    logging.info("My debugging message")
    '''

    max_entries = 0
    old_key = None
    datetime = ''

    text_file = open("output.txt", "r")
    lines = text_file.readlines()

    for line in lines:
        data = line.strip().split("\t")

        # each line must have 4 elements
        if len(data) != 4:
            continue

        # we have a new key. reset the counter.
        # set max_entries with first value of ENTRIESn_hourly on the new turnstile unit
        if old_key and old_key != data[0]:
            print "{0}\t{1}\t{2}".format(old_key, datetime, max_entries)
            max_entries = 0
            # datetime = time.strptime("{0} {1}".format(data[2], data[3]), "%Y-%m-%d %H:%M:%S") not needed.

        # same key.
        # if new ENTRIESn_hourly is equal to old ENTRIESn_hourly,
        #   set max_entries and datetime based on the latest datetime
        # if new ENTRIESn_hourly is greater than ENTRIESn_hourly, set max_entries and datetime
        if float(data[1]) == max_entries:
            if "{0} {1}".format(data[2], data[3]) > datetime:
                max_entries = float(data[1])
                datetime = "{0} {1}".format(data[2], data[3])
        elif float(data[1]) > max_entries:
            max_entries = float(data[1])
            datetime = "{0} {1}".format(data[2], data[3])
        old_key = data[0]

    # print value for last key
    if old_key is not None:
        print "{0}\t{1}\t{2}".format(old_key, datetime, max_entries)


reducer()



#https://docs.python.org/2/library/time.html#time.strptime
