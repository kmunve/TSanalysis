#!/usr/bin/python

import requests

method = '?invoke=getStationsFromTimeserieTypeElemCodes&'
params = {'timeserietypeID': '2', 'elem_codes': 'FF', 'username': ""}
url= 'http://eklima.met.no/met/MetService'

r = requests.Request('GET', url=url, params=params) 

d = r.prepare()
d.url = d.url.replace('?', method)
print d.url

s = requests.Session()
sr = s.send(d)

print sr.text
