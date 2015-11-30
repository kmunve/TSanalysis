#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import json
'''


__author__ = 'kmu'
'''

stat = json.load(open('../Test/Data/crocus_stations.json', 'r'))
crocus_st = stat['crocus_stations']
upgraded_st = stat['upgraded_precip']
third_st = stat['third_party_stations']

crocus_up = [station for station in upgraded_st if station not in crocus_st]
print(crocus_up)

crocus_st += crocus_up

crocus_third = [station for station in third_st if station not in crocus_st]
print(crocus_third)


crocus_st += crocus_third

print(crocus_st)
print(len(crocus_st))

# fid = open('../Test/Data/crocus_stations_all.json', 'w')
# json.dump({"crocus_stations": crocus_st}, fid)
# fid.close()
