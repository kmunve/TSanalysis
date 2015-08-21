#!/usr/bin/env python
import datetime as dt
import numpy as np
import pandas as pd

from crocus_forcing_nc import populate_forcing_nc

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


# dictionary pairing MET parameter names to Crocus parameter names
para_dict = {}# {'index': []}
index = []

tree = ET.ElementTree(file='test.xml')

root = tree.getroot()

for child_of_root in root:
    print child_of_root.tag, child_of_root.attrib



# Find timeStamp-tag
for timestamp in tree.iter('timeStamp'):
    

# Iterate over each item of the timeStamp
    for item in timestamp.findall('item'):

# Access its time stamp in the from-tag
        tstamp = item.find('from').text
# Convert string to datetime
        tstamp = dt.datetime.strptime(tstamp, '%Y-%m-%dT%H:%M:%S.000Z')
        index.append(tstamp)
#para_dict['index'].append(tstamp)

# Access each location-tag and store the station number in its id-tag
        loc = item.find('location')
        for locitem in loc:
# Get the station ID
            stat_id = locitem.find('id').text
# Convert stat_id to an integer
            stat_id = np.int(stat_id)
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


print para_dict

# Now store the whole shit in a pandas dataframe...
df = pd.DataFrame(para_dict, index=index)
print df


populate_forcing_nc(df)

#df.to_hdf('test_ET.hdf', 'test_from_eklima')

#for elem in tree.iter(tag='value'):
#    print elem.tag, elem.attrib, elem.text
