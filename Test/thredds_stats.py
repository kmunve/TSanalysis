#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'kmu'

"""
Retrieve data from netcdf files from thredds.met.no and do some statistics.
"""
import ipdb
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
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
filename = './Data/arome_metcoop_default2_5km_latest.nc'
nc = netCDF4.Dataset(filename)

# Get content
nc_info(nc)

# Get coordinates and other standard variables
x = nc.variables['x']
y = nc.variables['y']
lat = nc.variables['latitude']
lon = nc.variables['longitude']


# Bounding box for Rauland
lat1 = np.where(lat[:]>59.55)[1][0]
lat2 = np.where(lat[:]<60.02)[1][-1]
lon1 = np.where(lon[:]>7.47)[0][0]
lon2 = np.where(lon[:]<9.02)[0][-1]
print(lat1, lat2, lon1, lon2)

ipdb.set_trace()
altitude = nc.variables['altitude'][:, :] # retrieve model topography
bkgmap = nc.variables['land_area_fraction'][:, :]
times = nc.variables['time']
jd = netCDF4.num2date(times[:], times.units)

# Extract specific data

precip_org = nc.variables['precipitation_amount']
precip_acc = nc.variables['precipitation_amount_acc']
print(precip_acc[:].shape)

# Extract the subset/region we are interested in...
precip = precip_org[6:30, lon1:lon2, lat1:lat2]

#ipdb.set_trace()
print (precip.shape)
# sum up precip for 24 h after spin-up time
precip_sum = np.sum(precip, axis=0)

precip_thresh_05 = np.where(precip_sum > 5.0)
precip_thresh_10 = np.where(precip_sum > 10.0)
precip_thresh_20 = np.where(precip_sum > 20.0)
precip_thresh_30 = np.where(precip_sum > 30.0)


print(precip_thresh_20[0].size)
print(precip_sum.size)
print("05", (np.float(precip_thresh_05[0].size) / np.float(precip_sum.size))*100.)
print("10", (np.float(precip_thresh_10[0].size) / np.float(precip_sum.size))*100.)
print("20", (np.float(precip_thresh_20[0].size) / np.float(precip_sum.size))*100.)
print("30", (np.float(precip_thresh_30[0].size) / np.float(precip_sum.size))*100.)
ipdb.set_trace()

'''
a = precip[0, :, :]

# Extract required area
a = np.ones(bkgmap.shape) * np.nan

fracy1 = 320
fracy2 = 390
fracx1 = 180
fracx2 = 250

a[fracy1:fracy2, fracx1:fracx2] = h[0, fracy1:fracy2, fracx1:fracx2]
print(a.shape, type(a))

# Filter by elevation(band)
za = np.ma.masked_outside(altitude, 1000, 1500)
a[za.mask == True] = np.nan

T0 = 273.15
# Do statistics
print("Mean: {0}".format(np.nanmean(a)))
print("Standard deviation: {0}".format(np.nanstd(a, dtype=np.float64)))
print("Variance: {0}".format(np.nanvar(a)))
print("Average: {0}".format(np.average(a)))
print("Min: {0}".format(np.nanmin(a)))
print("Max: {0}".format(np.nanmax(a)))

'''

'''
Can use 'altitude' to filter out alpine regions or elevation bands
'''
'''
# View map and data
fig = plt.figure(figsize=(10, 12))
ax = fig.add_subplot(111)

xyext = [x[0], x[-1], y[0], y[-1]]
plt.imshow(bkgmap, zorder=0, origin='lower', cmap='pink', extent=xyext)
plt.imshow(a, alpha=0.8, zorder=1, origin='lower', cmap='seismic', extent=xyext)
#plt.legend()

plt.savefig(r'/home/karsten/test/ta_exa.png', dpi=90)
'''
