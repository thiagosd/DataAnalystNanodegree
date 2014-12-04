import csv
import sys
import string


def mapper():
    # Also make sure to fill out the reducer code before clicking "Test Run" or "Submit".

    # Each line will be a comma-separated list of values. The
    # header row WILL be included. Tokenize each row using the
    #commas, and emit (i.e. print) a key-value pair containing the
    #district (not state) and Aadhaar generated, separated by a tab.
    #Skip rows without the correct number of tokens and also skip
    #the header row.

    #You can see a copy of the the input Aadhaar data
    #in the link below:
    #https://www.dropbox.com/s/vn8t4uulbsfmalo/aadhaar_data.csv

    #Since you are printing the output of your program, printing a debug
    #statement will interfere with the operation of the grader. Instead,
    #use the logging module, which we've configured to log to a file printed
    #when you click "Test Run". For example:
    #logging.info("My debugging message")

    #for line in sys.stdin:  # cycle through lines of code

    # write to csv file, that will be used by the reducer
    output_file = open("output.txt", "wb")

    text_file = open("aadhaar_data.csv", "r")
    rows = text_file.readlines()[1:]  # readlines and skip the header (1st line)

    for row in rows:
        data = row.strip().split(",")

        # csv file has 12 header columns
        # we only want rows with values in all header columns
        if len(data) != 12:
            continue

        # print key-value pair
        # index 3 = District
        # index 8 = Aadhaar generated
        print "{0}\t{1}".format(data[3], data[8])
        output_file.write("{0}\t{1}".format(data[3], data[8]) + "\n")


mapper()