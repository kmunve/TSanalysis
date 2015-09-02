#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = 'kmu'

"""
Retrieve data from netcdf files from thredds.met.no and do some statistics.
"""

#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
import numpy as np
import netCDF4

def nc_info(nc_data):
    print('### DIMENSIONS ###')
    for k in nc_data.dimensions.keys():
        print(k)

    print('### VARIABLES ###')
    for k in nc_data.variables.keys():
        print(k)


# Access netcdf file via OpenDAP
filename = 'http://thredds.met.no/thredds/dodsC/arome25/arome_metcoop_default2_5km_latest.nc'
nc = netCDF4.Dataset(filename)

# Get content
nc_info(nc)

# Get coordinates and other standard variables
x = nc.variables['x']
y = nc.variables['y']

altitude = nc.variables['altitude'][:, :] # retrieve model topography
bkgmap = nc.variables['land_area_fraction'][:, :]
times = nc.variables['time']
jd = netCDF4.num2date(times[:], times.units)

# Extract specific data
vname = 'air_temperature_2m'
h = nc.variables[vname]

a = h[0, :, :]

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
