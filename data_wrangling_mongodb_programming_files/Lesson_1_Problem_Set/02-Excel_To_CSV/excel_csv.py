# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.
import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = 'Station|Year|Month|Day|Hour|Max Load'

    # start by col = 1. skip Hour_End column
    # sheet.ncols -1, to skip last column (ERCOT). not needed for this exercise.
    for col in range(1, sheet.ncols -1):
        cv = sheet.col_values(col, start_rowx=1, end_rowx=None)

        # get max load value and its position
        maxloadval = max(cv)
        maxloadpos = cv.index(maxloadval) + 1

        # get Station
        station = sheet.row_values(0, start_colx=col, end_colx=col + 1)[0]
        # get load time
        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(sheet.cell_value(maxloadpos, 0), 0)

        row_sequency = (station, year, month, day, hour, maxloadval)

        data += '\n' + '|'.join(str(v) for v in row_sequency)
    return data


def save_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)


def test():
    # open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    ans = {'FAR_WEST': {'Max Load': "2281.2722140000024", 'Year': "2013", "Month": "6", "Day": "26", "Hour": "17"}}

    fields = ["Year", "Month", "Day", "Hour", "Max Load"]
    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            s = line["Station"]
            if s == 'FAR_WEST':
                for field in fields:
                    assert ans[s][field] == line[field]


test()




#http://www.simplistix.co.uk/presentations/python-excel.pdf