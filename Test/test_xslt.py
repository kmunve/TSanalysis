#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Usage: python test_xslt.py > out.html
'''


import lxml.etree as ET

#xml_filename = 'bookstore.xml'
#xsl_filename = 'metdata.xsl'
xml_filename = 'getStationsProperties.out.all.xml'
xsl_filename = 'getStationsProperties.xsl'

dom = ET.parse(xml_filename)
xslt = ET.parse(xsl_filename)
transform = ET.XSLT(xslt)
newdom = transform(dom)
print(ET.tostring(newdom, pretty_print=True))
