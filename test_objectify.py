#!/bin/python
import requests
from StringIO import StringIO
from lxml import etree
from lxml import objectify
from wsklima_getdata import test_getMetDataValue


metdata_xsd = requests.get("http://eklima.met.no/wsKlima/schema/metdata.xsd")
f = StringIO(metdata_xsd.content)
metdata_scheme = etree.XMLSchema(file=f)
parser = objectify.makeparser(schema=metdata_scheme)


wr = test_getMetDataValue()

root = etree.fromstring(wr.content)
for element in root.findall("timestamp"):
    print element['location']
"""
soap-env:envelope.soap-env:body.ns1:getmetdatavaluesresponse.return.metdata.[timestamp@from].[location@id].[weatherelement@id@quality].value
"""


