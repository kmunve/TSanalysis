#!/usr/bin/python
"""
Author: kmunve

Return a list of available meteorological parameters from www.eklima.no
"""
from lxml import etree
from wsklima_getdata import wsKlimaRequest

def hourly_params():
    wr = wsKlimaRequest('getElementsFromTimeserieType', {'timeserietypeID': 2}).get()
    print wr.raw
#    tree = etree.parse(wr.raw, etree.XMLParser())
#    root = tree.getroot()
    root = etree.fromstring(wr.text)
# Print tree structure of file
    print etree.tostring(root, pretty_print=True)


if __name__ =="__main__":
    hourly_params()
