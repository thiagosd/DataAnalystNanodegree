import sys


def reducer():
    # Also make sure to fill out the mapper code before clicking "Test Run" or "Submit".

    # Each line will be a key-value pair separated by a tab character.
    #Print out each key once, along with the total number of Aadhaar
    #generated, separated by a tab. Make sure each key-value pair is
    #formatted correctly! Here's a sample final key-value pair: 'Gujarat\t5.0'

    #Since you are printing the output of your program, printing a debug
    #statement will interfere with the operation of the grader. Instead,
    #use the logging module, which we've configured to log to a file printed
    #when you click "Test Run". For example:
    #logging.info("My debugging message")

    #for line in sys.stdin:
    aadhaar_generated = 0
    old_key = None

    text_file = open("output.txt", "r")
    lines = text_file.readlines()
    for line in lines:
        data = line.strip().split("\t")

        # each line must have a key-pair value
        if len(data) != 2:
            continue

        if old_key and old_key != data[0]:
            print "{0}\t{1}".format(old_key, aadhaar_generated)
            aadhaar_generated = 0

        aadhaar_generated += int(data[1])
        old_key = data[0]

    if old_key is not None:
        print "{0}\t{1}".format(old_key, aadhaar_generated)


reducer()