#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from wsklima_requests import wsKlimaRequest
from wsklima_parser import parse_get_stations_properties, parse_get_elements_from_timeserie_type_station
'''
This script covers the following steps
- Retrieve information about station Oppdal stid=63705.
- Download relevant data over the period 04.12.2015 12:00 to 07.12.2015 12:00.
- Get closest AROME cell to station location.
- Retrieve missing data from AROME model in respective cell.
- Create Crocus forcing file from data.
-Create OPTIONS.nam file with initial snow-profile.

__author__ = 'kmu'
'''
stations = [63705,]

t_from = '2015-12-04'
t_to = '2015-12-07'

tt_id = 2


'''
STEP 1
'''
rsp = wsKlimaRequest('getStationsProperties', {'stations': stations, 'username': ""}).get()

st_props = parse_get_stations_properties(rsp.content)

print(st_props[str(stations[0])])


rsp = wsKlimaRequest('getElementsFromTimeserieTypeStation', {'stations': stations, 'timeserietypeID': tt_id}).get()

st_elems = parse_get_elements_from_timeserie_type_station(rsp.content)

relevant_sensors = ['TA',
                    'RR_1', 'RR_6', 'RRINTENS', 'DAGRRRR00', 'DAGRRSS00',
                    'X1UU', 'X1UM', 'UU',
                    'FX_6', 'FX_12', 'X1FX_1', 'X1FF', 'DD', 'FF',
                    'SAM', 'SA', 'RTS_1', 'SS_1', 'SS_24',
                    'X1QO', 'QNET', 'QSI', 'QSO', 'QRA', 'QOB', 'QLI', 'QLO', 'QD', 'QR', 'QT']

print(st_elems)

st_sensors = [sensor for sensor in relevant_sensors if sensor in st_elems.keys()]


'''
STEP 2
'''
wr = wsKlimaRequest('getMetData', {'timeserietypeID': tt_id, 'format': "", 'from': t_from, 'to': t_to,
                                   'stations': stations, 'elements': st_sensors,
                                   'hours': range(0, 24), 'months': "", 'username': ""}).get()

# if save:
#     fname = '54110.xml'
#     _f = open(fname, 'w')
#     _f.write(wr.text)
#     _f.close()
#     print('Data written to %s' % fname)
# print(wr.url)
