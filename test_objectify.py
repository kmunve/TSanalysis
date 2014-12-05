#!/usr/bin/python
import xml2dict
import json
from StringIO import StringIO
from lxml import etree
from lxml import objectify
from wsklima_getdata import test_getMetDataValue

from pandas import DataFrame


def print_dict(dictionary, ident = '', braces=1):
    """ Recursively prints nested dictionaries."""

    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            print '%s%s%s%s' %(ident,braces*'[',key,braces*']')
            print_dict(value, ident+'  ', braces+1)
        else:
            print ident+'%s = %s' %(key, value)

#
# metdata_xsd = requests.get("http://eklima.met.no/wsKlima/schema/metdata.xsd")
# f = StringIO(metdata_xsd.content)
# metdata_scheme = etree.XMLSchema(file=f)
# parser = objectify.makeparser(schema=metdata_scheme)

objectify.enable_recursive_str()
wr = test_getMetDataValue()
print wr.url
#print type(wr.text)
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


