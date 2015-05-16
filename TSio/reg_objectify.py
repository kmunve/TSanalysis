#!/usr/bin/python
# __author__ = 'kmu'

import re
from StringIO import StringIO
from lxml import etree
from lxml import objectify
from wsklima_getdata import test_getMetDataValue

from pandas import DataFrame


def print_dict(dictionary, ident='', braces=1):
    """ Recursively prints nested dictionaries."""

    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            print '%s%s%s%s' % (ident, braces * '[', key, braces * ']')
            print_dict(value, ident + '  ', braces + 1)
        else:
            print ident + '%s = %s' % (key, value)

#
# metdata_xsd = requests.get("http://eklima.met.no/wsKlima/schema/metdata.xsd")
# f = StringIO(metdata_xsd.content)
# metdata_scheme = etree.XMLSchema(file=f)
# parser = objectify.makeparser(schema=metdata_scheme)

objectify.enable_recursive_str()

r"""http://api01.nve.no/hydrology/forecast/avalanche/v2.0.2/api/AvalancheWarningByCoordinates/Detail/69.455819/19.907227/1/2014-03-13/2014-03-13"""
wr = test_getMetDataValue()
print wr.url

"""
<item xsi:type="ns2:no_met_metdata_WeatherElement">
<id xsi:type="xsd:string">TA</id>
<quality xsi:type="xsd:int">0</quality>
<value xsi:type="xsd:string">4.2</value>
</item>
"""


"""
from-tag and location-tag
"""
#re_from = re.compile('<from xsi:type="xsd:dateTime">(\d+-\d+-\d+T\d+:\d+:\d+:\d+Z)</from>', wr.text)
re_loc = re.compile('<location xsi:type="ns3:Array" ns3:arrayType="ns2:no_met_metdata_Location\[1\]">(.*?)</location>', re.DOTALL | re.IGNORECASE)

# wid = re.compile('<id xsi:type="xsd:string"\b[^>]*>(.*?)</id>')
wid = re.compile('<id xsi:type="xsd:string">(.*?)</id>', re.DOTALL | re.IGNORECASE)
wqt = re.compile('<quality xsi:type="xsd:int">(.*?)</quality>', re.DOTALL | re.IGNORECASE)
wval = re.compile('<value xsi:type="xsd:string">(.*?)</value>', re.DOTALL | re.IGNORECASE)



wid_l = []
qt_l = []
val_l = []

for welm in re.findall(re_loc, wr.text):
    wid_l.append(re.findall(wid, welm))
    qt_l.append(re.findall(wqt, welm))
    val_l.append(re.findall(wval, welm))



#ex_wid = re.findall(wid, wr.text)


#print type(wr.raw)
#print wr.content


"""
soap-env:envelope.soap-env:body.ns1:getmetdatavaluesresponse.return.metdata.[timestamp@from].[location@id].[weatherelement@id@quality].value
"""


