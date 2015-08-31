#!/usr/bin/env python
import lxml.etree as ET

xml_filename = 'bookstore.xml'
xsl_filename = 'metdata.xsl'

dom = ET.parse(xml_filename)
xslt = ET.parse(xsl_filename)
transform = ET.XSLT(xslt)
newdom = transform(dom)
print(ET.tostring(newdom, pretty_print=True))
