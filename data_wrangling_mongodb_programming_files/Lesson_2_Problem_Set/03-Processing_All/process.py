#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Let's assume that you combined the code from the previous 2 exercises
# with code from the lesson on how to build requests, and downloaded all the data locally.
# The files are in a directory "data", named after the carrier and airport:
# "{}-{}.html".format(carrier, airport), for example "FL-ATL.html".
# The table with flight info has a table class="dataTDRight".
# There are couple of helper functions to deal with the data files.
# Please do not change them for grading purposes.
# All your changes should be in the 'process_file' function
# This is example of the data structure you should return
# Each item in the list should be a dictionary containing all the relevant data
# Note - year, month, and the flight data should be integers
# You should skip the rows that contain the TOTAL data for a year
# data = [{"courier": "FL",
# "airport": "ATL",
# "year": 2012,
# "month": 12,
# "flights": {"domestic": 100,
# "international": 100}
# },
# {"courier": "..."}
# ]
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os

datadir = "data"


def open_zip(datadir):
    with ZipFile('{0}.zip'.format(datadir), 'r') as myzip:
        myzip.extractall()


def process_all(datadir):
    files = os.listdir(datadir)
    return files


def process_file(f):
    # This is example of the data structure you should return
    # Each item in the list should be a dictionary containing all the relevant data
    # Note - year, month, and the flight data should be integers
    # You should skip the rows that contain the TOTAL data for a year
    # data = [{"courier": "FL",
    # "airport": "ATL",
    # "year": 2012,
    # "month": 12,
    #         "flights": {"domestic": 100,
    #                     "international": 100}
    #         },
    #         {"courier": "..."}
    # ]
    data = []
    info = {}
    info["courier"], info["airport"] = f[:6].split("-")

    with open("{}/{}".format(datadir, f), "r") as html:
        soup = BeautifulSoup(html)
        flightsrow = soup.find_all("tr", attrs={"class": "dataTDRight"})
        for row in flightsrow:
            #<td>Year</td><td>Month</td><td>DOMESTIC</td><td>INTERNATIONAL</td><td>TOTAL</td>
            columns = row.find_all('td')
            if columns[1].getText() == "TOTAL":
                continue
            data.append({"courier": info["courier"],
                         "airport": info["airport"],
                         "year": int(columns[0].getText()),
                         "month": int(columns[1].getText()),
                         "flights": {
                             "domestic": int(columns[2].getText().replace(',', '')),
                             "international": int(columns[3].getText().replace(',', ''))
                         }
            })
    return data


def test():
    print "Running a simple test..."
    # open_zip(datadir)
    files = process_all(datadir)
    data = []
    for f in files:
        data += process_file(f)
    assert len(data) == 3
    for entry in data[:3]:
        assert type(entry["year"]) == int
        assert type(entry["flights"]["domestic"]) == int
        assert len(entry["airport"]) == 3
        assert len(entry["courier"]) == 2
    print "... success!"


if __name__ == "__main__":
    test()