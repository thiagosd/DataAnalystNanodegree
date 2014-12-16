import sys


def reducer():
    '''
    Given the output of the mapper for this exercise, the reducer should return
    one row per unit, along with the total number of ENTRIESn_hourly over the
    course of May (which is the duration of our data).

    You can assume that the input to the reducer is sorted by UNIT, such that all rows
    corresponding to a particular UNIT are grouped together.

    The output should have a unit (the key) follow by a tab, follow by a value.
    An example output row from the reducer might look like this:
    R001\t500625.0

    Since you are printing the actual output of your program, you
    can't print a debug statement without breaking the grader.
    Instead, you should use the logging module, which we've configured
    to log to a file which will be printed when you hit "Test Run".
    For example:
    logging.info("My debugging message")
    '''

    entries = 0
    old_key = None

    text_file = open("output.txt", "r")
    lines = text_file.readlines()

    for line in lines:
        data = line.strip().split("\t")

        # each line must have a key-pair value
        if len(data) != 2:
            continue

        # we have a new key. reset the counter.
        if old_key and old_key != data[0]:
            print "{0}\t{1}".format(old_key, entries)
            entries = 0

        # same key. increment the counter. update the key
        entries += float(data[1])
        old_key = data[0]

    # print value for last key
    if old_key is not None:
        print "{0}\t{1}".format(old_key, entries)


reducer()
