#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')

import datetime as dt
import numpy as np
import pandas as pd

from lxml import etree
# test the lxml package in comparision to the standard ElementTree pkg


from crocus_forcing_nc import populate_forcing_nc


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

    # Get all item-tags that are a children of the current location-tag
    LOCitmes = TS.xpath('location/item')
    for LOC in LOCitmes:
        # Retrieve station id
        stat_id = LOC.xpath('id')[0].text
        print stat_id
        if stat_id not in stat_dict.keys():
            stat_dict[stat_id] = {}

        # Get all item-tags that are a children of the weatherElement-tag
        WEitems = LOC.xpath('weatherElement/item')
        # Loop over the weather elements
        for WE in WEitems:
            we_id = WE.xpath('id')[0].text # Retrieve parameter name
            we_q = WE.xpath('quality')[0].text # Retrieve quality flag
            we_val = WE.xpath('value')[0].text # Retrieve measured value
            print we_id, we_val

            if we_id not in stat_dict[stat_id].keys():
                stat_dict[stat_id] = {}
                stat_dict[stat_id]['index'] = []
                stat_dict[stat_id][we_id] = {}
                stat_dict[stat_id][we_id]['val'] = []
                stat_dict[stat_id][we_id]['q'] = []

            stat_dict[stat_id]['index'].append(_index)
            stat_dict[stat_id][we_id]['val'].append(we_val)
            stat_dict[stat_id][we_id]['q'].append(we_q)


print stat_dict['12290'].keys()
print stat_dict['12290']['RR_1']['val'][0]


# Print tree structure of file
#print etree.tostring(root, pretty_print=True)
"""
for child_of_root in root:
    print child_of_root.tag, '---', child_of_root.attrib



# Find timeStamp-tag
for timestamp in tree.iter('timeStamp'):


# Iterate over each item of the timeStamp
    for item in timestamp.findall('item'):

# Access its time stamp in the from-tag
        tstamp = item.find('from').text
# Convert string to datetime
        tstamp = dt.datetime.strptime(tstamp, '%Y-%m-%dT%H:%M:%S.000Z')
        index.append(tstamp)

# Access each location-tag and store the station number in its id-tag
        loc = item.find('location')
        for locitem in loc:
            '''
            Start to iterate over the items in the location tag
            see http://lxml.de/xpathxslt.html to get a better mapping.
            '''

            for stat_item in locitem.findall('item'):
                pass
            # Get the station ID

            stat_id = locitem.find('id').text
            if stat_id not in stat_dict.keys():
                stat_dict[stat_id] = {}
'''
# Convert stat_id to an integer
            stat_id = np.int(stat_id)
'''

    # Access the weatherElement
                weather_e = locitem.find('weatherElement')
                for weather_i in weather_e:
    # Access the parameter ID
                    param_id = weather_i.find('id').text
                    if param_id not in para_dict.keys():
                        para_dict[param_id] = []
    # Access the quality tag
                    quality = weather_i.find('quality').text
    # Convert the quality tag to an interger
                    quality = np.int(quality)
    # Access the value
                    value = weather_i.find('value').text
    # Convert the value to float
                    value = np.float(value)
    # Print for testing
                    #print stat_id, tstamp, param_id, quality, value

                    para_dict[param_id].append(value)
                stat_dict[stat_id] = para_dict


'''
When retrieving data from more than two stations the dictionary is wrong.
'''

print para_dict
print stat_dict.keys()



# Now store in a pandas dataframe...
df = pd.DataFrame(stat_dict['12290'], index=index)
#print df

#df.plot(secondary_y=['TA', 'UU'])
df.plot(subplots=True)
matplotlib.pyplot.gcf().savefig('12290.png', dpi=90)
#populate_forcing_nc(df)

#df.to_hdf('test_lxml.hdf', 'test_from_eklima')

"""
