#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
Author: kmunve

Returns a list of available meteorological parameters from www.eklima.no
CSV files with English and Norwegian terms are created.
"""
from lxml import etree
from wsklima_getdata import wsKlimaRequest


def hourly_params():
    # Make an eklima request
    wr = wsKlimaRequest('getElementsFromTimeserieType', {'timeserietypeID': 2}).get()
    
    # Parse XML string
    root = etree.fromstring(wr.content)
    
    # Temporary list of element codes
    elem_list = []

    # Open file for Norwegian version
    fid = open('eklima_param_list_no.csv', 'w')
    fid.write('#Gruppe,#Undergruppe,#Kode,#Enhet,#Nummer,#Beskrivelse\n')

    # Iterate over all "item" elements
    for element in root.iter("item"):
        fid.write("{0},{1},{2},{3},{4},{5}\n".format(element.find('elemGroup').text.encode('utf-8'), element.find('name').text.encode('utf-8'), element.find('elemCode').text.encode('utf-8'), element.find('unit').text.encode('utf-8'), element.find('elemNo').text.encode('utf-8'), element.find('description').text.encode('utf-8')))
            
        elem_list.append(element.find('elemCode').text)

    fid.close()
 
    wr =  wsKlimaRequest('getElementsProperties', {'language': 'en', 'elem_codes': elem_list}).get()

    # Parse XML string
    root = etree.fromstring(wr.content)

    # Print tree structure of file
    #print etree.tostring(root, pretty_print=True)

    # Open file for English version
    fid = open('eklima_param_list_en.csv', 'w')
    fid.write('#Group,#Subgroup,#Code,#Unit,#Number,#Description\n')

    # Iterate over all "item" elements
    for element in root.iter("item"):
        fid.write("{0},{1},{2},{3},{4},{5}\n".format(element.find('elemGroup').text.encode('utf-8'), element.find('name').text.encode('utf-8'), element.find('elemCode').text.encode('utf-8'), element.find('unit').text.encode('utf-8'), element.find('elemNo').text.encode('utf-8'), element.find('description').text.encode('utf-8')))

    fid.close()
    print '...files written'
    

if __name__ =="__main__":
    hourly_params()
