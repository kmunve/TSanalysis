#!/usr/bin/python
import xml2dict
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
wr = test_getMetDataValue()
print wr.url

"""
<item xsi:type="ns2:no_met_metdata_WeatherElement">
<id xsi:type="xsd:string">TA</id>
<quality xsi:type="xsd:int">0</quality>
<value xsi:type="xsd:string">4.2</value>
</item>
"""

ii = re.compile('<item xsi:type="ns2:no_met_metdata_WeatherElement">(.*?)</item>', re.DOTALL | re.IGNORECASE)

# wid = re.compile('<id xsi:type="xsd:string"\b[^>]*>(.*?)</id>')
wid = re.compile('<id xsi:type="xsd:string">(.*?)</id>', re.DOTALL | re.IGNORECASE)
wqt = re.compile('<quality xsi:type="xsd:int">(.*?)</quality>', re.DOTALL | re.IGNORECASE)
wval = re.compile('<value xsi:type="xsd:string">(.*?)</value>', re.DOTALL | re.IGNORECASE)

it = re.finditer(ii, wr.text)

wid_l = []
qt_l = []
val_l = []

for welm in ii:
    wid_l.append(re.findall(wid, welm))
    qt_l.append(re.findall(wqt, welm))
    val_l.append(re.findall(wval, welm))



#ex_wid = re.findall(wid, wr.text)


#print type(wr.raw)
#print wr.content


o = xml2dict.parse(wr.content)
c = o['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:getMetDataResponse']['return']['timeStamp']

print_dict(c)

for child in c['item']:
    print child['from']['#text']
    print child['location'].keys()
    for k, v in child['location'].iteritems():
        #try:
        print type(k['weatherElement'])
        for we in k['weatherElement']:
            print we['item']['value']['#text']
            #except TypeError:
            #    continue

df = DataFrame(o['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:getMetDataResponse']['return']['timeStamp'])

#for i in df.item:
#    print i['from']

fid = StringIO(wr.content)
parsed = objectify.parse(fid)
root = parsed.getroot()
ret = root.findall('timeStamp')

#print root['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:getMetDataResponse']['return']
print "ROOT"
print ret
for child in root.getchildren():
    print child.tag
    print child.getchildren()

#root = etree.fromstring(wr.content)
#for element in root.findall("timestamp"):
#    print element['location']
"""
soap-env:envelope.soap-env:body.ns1:getmetdatavaluesresponse.return.metdata.[timestamp@from].[location@id].[weatherelement@id@quality].value
"""


