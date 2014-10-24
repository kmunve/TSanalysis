#!/usr/bin/python
"""
Author. kmunve
"""
from lxml import etree
from wsklima_getdata import wsKlimaRequest


wr = wsKlimaRequest('getStationsFromTimeserieTypeElemCodes', {'timeserietypeID': 2, 'elem_codes': ['RR_1', 'RR_24', 'TA', 'UU', 'FF'], 'use\
rname': ""}).get()


# Parse XML string
root = etree.fromstring(wr.content)

# Temporary list of element codes
station_list = []

# Iterate over all "item" elements
for element in root.iter("item"):
    #        fid.write("{0},{1},{2},{3},{4},{5}\n".format(element.find('elemGroup').text.encode('utf-8'), element.find('name').text.encode('utf-8')element.find('elemCode').text.encode('utf-8'), element.find('unit').text.encode('utf-8'), element.find('elemNo').text.encode('utf-8'), element.find('description').text.encode('utf-8')))
    # Add only stations that still are operative
    if int(element.find('toYear').text) == 0:
        station_list.append(int(element.find('stnr').text))

print "Found {0} stations.".format(len(station_list))
print station_list
