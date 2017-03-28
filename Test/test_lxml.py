#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
MOVED TO WSKLIMA_PARSER.PY



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



'''

import matplotlib
matplotlib.use('Agg')

import datetime as dt
import numpy as np

from lxml import etree
# test the lxml package in comparision to the standard ElementTree pkg


# try:
#     import xml.etree.cElementTree as ET
# except ImportError:
#     import xml.etree.ElementTree as ET


# dictionary pairing MET parameter names to Crocus parameter names
stat_dict = {} # station dictionary
#para_dict = {}# {'index': []}
index = []

tree = etree.parse(open('54110.xml'))

root = tree.getroot()

# Get all item-tags that are a children of the timeStamp-tag
TSitems = root.xpath('//timeStamp/item')
#print len(rootTS), rootTS[0].tag

#TS = rootTS[0].xpath('item[@xsi:type="ns2:no_met_metdata_TimeStamp"]')
#TS = rootTS[0].xpath('item')

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
        print stat_id
        if stat_id not in stat_dict.keys():
            stat_dict[stat_id] = {}
            stat_dict[stat_id]['index'] = []

        stat_dict[stat_id]['index'].append(_index)

        # Get all item-tags that are a child of the weatherElement-tag
        WEitems = LOC.xpath('weatherElement/item')
        # Loop over the weather elements
        for WE in WEitems:
            we_id = WE.xpath('id')[0].text # Retrieve parameter name
            we_q = np.int(WE.xpath('quality')[0].text) # Retrieve quality flag
            we_val = np.float(WE.xpath('value')[0].text) # Retrieve measured value
            print we_id, we_val
            # Add a new dictionary if the weather element does not exist, yet.
            if we_id not in stat_dict[stat_id].keys():
                stat_dict[stat_id][we_id] = {}
                stat_dict[stat_id][we_id]['val'] = []
                stat_dict[stat_id][we_id]['q'] = []

            # Append value and quality for the current time step
            stat_dict[stat_id][we_id]['val'].append(we_val)
            stat_dict[stat_id][we_id]['q'].append(we_q)

#ipdb.set_trace()
print stat_dict['12290'].keys()
print stat_dict['12290']['RR_1']['val'][0]

'''
Needs to be adapted to new dict-structure.
'''

# Now store in a pandas dataframe...
#df = pd.DataFrame(stat_dict['12290'])
#print df

#df.plot(secondary_y=['TA', 'UU'])
#df.plot(subplots=True)
#matplotlib.pyplot.gcf().savefig('12290.png', dpi=90)
#populate_forcing_nc(df)

#df.to_hdf('test_lxml.hdf', 'test_from_eklima')
