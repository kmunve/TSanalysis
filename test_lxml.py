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
para_dict = {}# {'index': []}
index = []

tree = etree.parse(open('54110.xml'))

root = tree.getroot()


rootTS = root.xpath('//timeStamp')
print len(rootTS), rootTS[0].tag

#TS = rootTS[0].xpath('item[@xsi:type="ns2:no_met_metdata_TimeStamp"]')
TS = rootTS[0].xpath('item')
for f in TS:
    time = f.xpath('from')[0].text
    L = f.xpath('location/item')
    for loc in L:
        stat_id = loc.xpath('id')[0].text
        print stat_id
        WEitems = loc.xpath('weatherElement/item')
        for WE in WEitems:
            we_name = WE.xpath('id')[0].text
            we_q = WE.xpath('quality')[0].text
            we_val = WE.xpath('value')[0].text
            print we_name, we_q, we_val




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
