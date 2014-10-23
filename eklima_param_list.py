#!/usr/bin/python
"""
Author: kmunve

Return a list of available meteorological parameters from www.eklima.no
"""
from lxml import etree
from wsklima_getdata import wsKlimaRequest
from io import StringIO


def hourly_params():
    # Make an eklima request
    wr = wsKlimaRequest('getElementsFromTimeserieType', {'timeserietypeID': 2}).get()
    
    # Parse XML string
    root = etree.fromstring(wr.content)
    tmp = etree.tostring(root)
    print tmp
    # Print tree structure of file
    #print etree.tostring(root, pretty_print=True)
    
    # Open file
    fid = open('eklima_param_list.csv', 'w')
    fid.write('#Main Group,#Group,#Code,#Unit,#Number,#Description\n')

    # Iterate over all "item" elements
    for element in root.iter("item"):
        print element
        print "{0},{1},{2},{3},{4},{5}\n".format(element.find('elemGroup').text, element.find('name').text, element.find('elemCode').text, element.find('unit').text, element.find('elemNo').text, element.find('description').text)

        fid.write("{0},{1},{2},{3},{4},{5}\n".format(element.find('elemGroup').text, element.find('name').text, element.find('elemCode').text, element.find('unit').text, element.find('elemNo').text, element.find('description').text))

    fid.close()
    print '...file written'
    

if __name__ =="__main__":
    hourly_params()
