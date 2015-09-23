#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
__author__: Karsten Müller, kmunve

Converts the XML return from a wsklima.getData() call to a Python dictionary.
For more info on wsklime see eklima.met.no.

Structure of the returned Pytho dictionary
A dictionary with a key for each station:
    stat_dict['<station-id>']
        ...containing a dictionary with the follwoing keys:
        ['index']: list of datetime object of the observation time
        ['<weather-element>']: dictionary with the follwoing keys:
            ['val']: list of values at observation time
            ['q']: list of quality flags corresponding to 'val'

Usage:

Get XML file from eklima.met.no, e.g. by using wsklima_requests.py or
http://eklima.met.no/met/MetService?operation=getMetData

Hand the XML file to parse_getData(xml_data)

'''

import datetime as dt
import numpy as np

from cStringIO import StringIO
from lxml import etree

def parse_getData(xml_data):
    stat_dict = {} # station dictionary
    index = []

    tree = etree.parse(open(xml_data))

    root = tree.getroot()

    # Get all item-tags that are a child of the timeStamp-tag
    TSitems = root.xpath('//timeStamp/item')

    # loop over all timestamps
    for TS in TSitems:
        # extract datetime
        tstamp = TS.xpath('from')[0].text
        # Convert string to datetime
        _index = dt.datetime.strptime(tstamp, '%Y-%m-%dT%H:%M:%S.000Z')

        # Get all item-tags that are a child of the current location-tag
        LOCitmes = TS.xpath('location/item')
        for LOC in LOCitmes:
            # Retrieve station id
            stat_id = LOC.xpath('id')[0].text

            # Init new station dict if necessary
            if stat_id not in stat_dict.keys():
                stat_dict[stat_id] = {}
                stat_dict[stat_id]['index'] = []

            # Append the time stamp
            stat_dict[stat_id]['index'].append(_index)

            # Get all item-tags that are a child of the weatherElement-tag
            WEitems = LOC.xpath('weatherElement/item')
            # Loop over the weather elements
            for WE in WEitems:
                we_id = WE.xpath('id')[0].text # Retrieve parameter name
                we_q = np.int(WE.xpath('quality')[0].text) # Retrieve quality flag
                we_val = np.float(WE.xpath('value')[0].text) # Retrieve measured value

                # Add a new dictionary if the weather element does not exist, yet.
                if we_id not in stat_dict[stat_id].keys():
                    stat_dict[stat_id][we_id] = {}
                    stat_dict[stat_id][we_id]['val'] = []
                    stat_dict[stat_id][we_id]['q'] = []

                # Append value and quality for the current time step
                stat_dict[stat_id][we_id]['val'].append(we_val)
                stat_dict[stat_id][we_id]['q'].append(we_q)

    return stat_dict

if __name__ == '__main__':
    import pylab
    sd = parse_getData('54110.xml')
    print sd['54110']
    print sd['12290']
    pylab.plot(sd['12290']['index'], sd['12290']['TA']['val'])
    pylab.show()
