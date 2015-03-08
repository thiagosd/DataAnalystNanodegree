#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
The output should be a dictionary with the tag name as the key
and number of times this tag can be encountered in the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.ElementTree as ET
import pprint


def count_tags(filename):
    # YOUR CODE HERE
    # What tags are there and how many
    # The output should be a dictionary with the tag name as the key
    # and number of times this tag can be encountered

    tags = {}
    for event, elem in ET.iterparse(filename):
        tag = elem.tag
        tags[tag] = tags[tag] + 1 if tag in tags.keys() else 1
    return tags


def test():
    tags = count_tags('miami_florida.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                    'member': 41369,
                    'nd': 1550300,
                    'node': 1305779,
                    'osm': 1,
                    'relation': 1340,
                    'tag': 1388579,
                    'way': 171890}


if __name__ == "__main__":
    test()