#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from wsklima_requests import wsKlimaRequest
'''


__author__ = 'kmu'

Hemsedal Hollekolten 25112, 807 moh, wind
Hemsedal Hølto 25100, 648 moh, precip, snow depth
Hemsedal II 25110, 604 moh, snow depth
'''

from_date = '2016-01-01'
to_date = '2016-01-31'


wr = wsKlimaRequest('getMetData', {'timeserietypeID': 2, 'format': "", 'from': from_date, 'to': to_date, 'stations': [25112,], 'elements': ['TA', 'FF', 'DD'], 'hours': range(0,24), 'months': "", 'username': ""}).get()
_fname = '../Test/Data/hemsedal_hollekolten_jan2016.xml'
_f = open(_fname, 'w')
_f.write(wr.text)
_f.close()
print('Data written to %s' % _fname)
print(wr.url)

wr = wsKlimaRequest('getMetData', {'timeserietypeID': 2, 'format': "", 'from': from_date, 'to': to_date, 'stations': [25100,], 'elements': ['RR_1', 'RR_24', 'SA'], 'hours': range(0,24), 'months': "", 'username': ""}).get()
_fname = '../Test/Data/hemsedal_hoelto_jan2016.xml'
_f = open(_fname, 'w')
_f.write(wr.text)
_f.close()
print('Data written to %s' % _fname)
print(wr.url)

wr = wsKlimaRequest('getMetData', {'timeserietypeID': 2, 'format': "", 'from': from_date, 'to': to_date, 'stations': [25110,], 'elements': ['RR_1', 'RR_24', 'SA'], 'hours': range(0,24), 'months': "", 'username': ""}).get()
_fname = '../Test/Data/hemsedal_II_jan2016.xml'
_f = open(_fname, 'w')
_f.write(wr.text)
_f.close()
print('Data written to %s' % _fname)
print(wr.url)


