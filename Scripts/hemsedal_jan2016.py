#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from wsklima_requests import wsKlimaRequest
from wsklima_parser import parse_get_data
import pylab as plt
import numpy as np
from pandas import Series
'''


__author__ = 'kmu'

Hemsedal Hollekolten 25112, 807 moh, wind
Hemsedal Hølto 25100, 648 moh, precip, snow depth
Hemsedal II 25110, 604 moh, snow depth
'''

def request_data():
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


def parse_data():
    sd = parse_get_data('../Test/Data/hemsedal_hollekolten_jan2016.xml')
    ff_s = Series(sd['25112']['FF']['val'], index=sd['25112']['index'])

    # replace fill values to NaN
    ff_s.replace(-99999.0, np.nan, inplace=True)
    ff24_s = ff_s.resample('D')

    sd = parse_get_data('../Test/Data/hemsedal_hoelto_jan2016.xml')
    ts = Series(sd['25100']['RR_24']['val'], index=sd['25100']['index'])

    # select only measurements at 06 every day
    ts = ts[ts.index.hour == 6]
    # ts.replace(-99999.0, np.nan, inplace=True)
    # ts.replace(-1.0, 0.0, inplace=True)
    print(ff24_s)

    plt.bar(ts.index, ts.values)
    plt.hold(True)

    plt.plot(ff_s.index, ff_s.values)
    plt.plot(ff24_s.index, ff24_s.values)
    # plt.bar(sd['25100']['index'], sd['25100']['RR_24']['val'])
    plt.show()


if __name__ == "__main__":
    # request_data()
    parse_data()