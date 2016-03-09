#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from pandas import Series, DataFrame
import time
import re
import requests
import json

'''


__author__ = 'kmu'
'''


url = "http://h-web01.nve.no/chartserver/ShowData.aspx?req=getchart&ver=1.0&vfmt=json&time=-3;0&chd=ds=htsre,id=17150.16,rt=1:0,mth=inst|ds=htsry,id=metx[17150].6038,mth=inst"
"""
The *|* indicates a request to another source or dataset and will result in a new list entry in the retrun from json.loads.
"""
"http://h-web01.nve.no/chartserver/ShowData.aspx?req=getchart&ver=1.0&&time=20160302T0600;20160310T0600&chs=150x150&lang=no&chlf=desc&chsl=0;+0&chd=ds=htsre,da=29,id=23500.17,rt=1:00,cht=line,mth=inst|ds=htsry,da=29,id=metx[23500;17].6000,rt=1:00,cht=line,mth=inst&nocache=0.6985500316478995&vfmt=json"

_req = requests.get(url)
res = _req.text


print(res)
print(type(res))


# convert json obsject to python object
data_list = json.loads(res)
print(data_list)
print(type(data_list), len(data_list))

# parse data as pandas time-series
data_keys = ['LegendText', 'SeriesPoints']
df = DataFrame(data_list[0]['SeriesPoints'], columns=data_list[0]['SeriesPoints'][0].keys())

#TODO: Convert the Date string to a pyhton datetime object prior reindexing


# make the date the new index
# df.index = df['Key']

# remove the duplicate Key column
# del df['Key']
print(df)

# print(time.gmtime(0))

def convert_timestr(s, as_string=True):
    """

    :param s: time string returned by chartserver query, e.g. /Date(1457485200000)/
    :return:
    """
    # regular expression to extract the numeric values in the json date string
    regex = re.compile("\d+")
    # extract numerical value, make it a float, and divide by 1000 to get seconds since 1.1.1970
    ds = time.gmtime(float(regex.search(s).group())*0.001)
    if as_string:
        ds = time.strftime("%Y-%m-%dT%H:%M:%S", ds)

    return ds

df['Key'] = [convert_timestr(s) for s in df['Key']]

print(df)
# s = re.findall('\(.*?\)', df['Key'][0])
# s = time.gmtime(df['Key'][0])
print('Done')


