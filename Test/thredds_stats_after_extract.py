#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'kmu'

"""
Retrieve data from netcdf files from thredds.met.no.
Extract data within an area using fimex: see extract.sh
Load and do some statistics.
"""
import ipdb
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import netCDF4

def nc_info(nc_data):
    print('### DIMENSIONS ###')
    print(nc_data.dimensions)
    for k in nc_data.dimensions.keys():
        print(k)

    print('### VARIABLES ###')
    for k in nc_data.variables.keys():
        print(k)


# Access netcdf file via OpenDAP
#filename = 'http://thredds.met.no/thredds/dodsC/arome25/arome_metcoop_default2_5km_latest.nc'
filename = './Data/rauland.nc'
nc = netCDF4.Dataset(filename)

# Get content
nc_info(nc)

# Get coordinates and other standard variables
x = nc.variables['x']
y = nc.variables['y']
lat = nc.variables['latitude']
lon = nc.variables['longitude']



#ipdb.set_trace()

times = nc.variables['time']
jd = netCDF4.num2date(times[:], times.units)

# Extract specific data and remove unnecessary dimensions
precip = nc.variables['precipitation_amount'][:].squeeze()
precip_acc = nc.variables['precipitation_amount_acc'][:].squeeze()


#ipdb.set_trace()

# sum up precip for 24 h after spin-up time
precip_sum = np.sum(precip, axis=0)

thresholds = {'0.01': 0., '5.0': 0., '10.0': 0., '20.0': 0., '40.0': 0.,}
precip_thres = np.empty_like(thresholds)
for t in thresholds.keys():
    _pt = np.where(precip_sum > np.float(t))
    thresholds[t] = (np.float(_pt[0].size) / np.float(precip_sum.size))*100.

thresholds_acc = {'0.01': 0., '5.0': 0., '10.0': 0., '20.0': 0., '40.0': 0.,}
precip_thres_acc = np.empty_like(thresholds)
for t in thresholds_acc.keys():
    _pt = np.where(precip_acc[-1,:,:] > np.float(t))
    thresholds_acc[t] = (np.float(_pt[0].size) / np.float(precip_sum.size))*100.

#ipdb.set_trace()

plt.bar(np.array(thresholds.keys(), dtype=np.float), thresholds.values(), width=1.2, color='red')
plt.hold(True)
plt.bar(np.array(thresholds_acc.keys(), dtype=np.float), thresholds_acc.values())
plt.figure()
plt.imshow(precip_sum); plt.colorbar()
plt.show()
