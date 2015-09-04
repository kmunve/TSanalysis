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

# Extract specific data

precip = nc.variables['precipitation_amount']
print (precip.shape)
precip_acc = nc.variables['precipitation_amount_acc']
print(precip_acc[:].shape)


#ipdb.set_trace()

# sum up precip for 24 h after spin-up time
precip_sum = np.sum(precip[:], axis=0)

precip_thresh_00 = np.where(precip_sum < 0.5)
precip_thresh_05 = np.where(precip_sum > 5.0)
precip_thresh_10 = np.where(precip_sum > 10.0)
precip_thresh_20 = np.where(precip_sum > 20.0)
precip_thresh_30 = np.where(precip_sum > 30.0)


print(precip_thresh_20[0].size)
print(precip_sum.size)

pt00 = (np.float(precip_thresh_00[0].size) / np.float(precip_sum.size))*100.
pt05 = (np.float(precip_thresh_05[0].size) / np.float(precip_sum.size))*100.
pt10 = (np.float(precip_thresh_10[0].size) / np.float(precip_sum.size))*100.
pt20 = (np.float(precip_thresh_20[0].size) / np.float(precip_sum.size))*100.
pt30 = (np.float(precip_thresh_30[0].size) / np.float(precip_sum.size))*100.

print("05", (np.float(precip_thresh_05[0].size) / np.float(precip_sum.size))*100.)
print("10", (np.float(precip_thresh_10[0].size) / np.float(precip_sum.size))*100.)
print("20", (np.float(precip_thresh_20[0].size) / np.float(precip_sum.size))*100.)
print("30", (np.float(precip_thresh_30[0].size) / np.float(precip_sum.size))*100.)

#ipdb.set_trace()


plt.bar([0, 5, 10, 20, 30], [pt00, pt05, pt10, pt20, pt30])
plt.show()
