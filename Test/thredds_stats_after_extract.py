#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__   = 'kmunve'
__created__  = datetime.datetime(2015, 7, 1)
__modified__ = datetime.datetime(2015, 7, 1)
__version__  = "1.0"
__status__   = "Development"


"""
Retrieve data from netcdf files from thredds.met.no.
Extract data within an area using fimex: see extract.sh
Load and do some statistics.
"""
#import ipdb
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
filename = './Data/lofoten_t.nc'
nc = netCDF4.Dataset(filename)

# Get content
#nc_info(nc)

# Get coordinates and other standard variables
x = nc.variables['x']
y = nc.variables['y']
lat = nc.variables['latitude']
lon = nc.variables['longitude']

# Extract land area fraction and use as mask in coastal regions
# 0 = 100% water cell, 1 = 100% land cell
land_mask = np.ma.masked_equal(nc.variables['land_area_fraction'][:].squeeze(), 0)
print(land_mask.mask)
# Get number of non-masked elements
land_cells = land_mask.count()
print(land_cells)

#ipdb.set_trace()


# TODO: extract time variable from thredds
#times = nc.variables['time']
#jd = netCDF4.num2date(times[:], times.units)

# Extract specific data and remove unnecessary dimensions
precip = nc.variables['precipitation_amount'][:].squeeze()
precip_low = nc.variables['precipitation_amount_low_estimate'][:].squeeze()
precip_mid = nc.variables['precipitation_amount_middle_estimate'][:].squeeze()
precip_high = nc.variables['precipitation_amount_high_estimate'][:].squeeze()

# Double check if thats accumulates since model init
# precip_acc = nc.variables['precipitation_amount_acc'][:].squeeze()

#ipdb.set_trace()

# TODO: make histogram see np.ravel to flatten array: plt.hist(img.ravel(), lw=0, bins=256);
# sum up precip for 24 h after spin-up time
precip_sum = np.ma.array(np.sum(precip, axis=0), mask=land_mask.mask)
precip_low_sum = np.ma.array(np.sum(precip_low, axis=0), mask=land_mask.mask)
precip_mid_sum = np.ma.array(np.sum(precip_mid, axis=0), mask=land_mask.mask)
precip_high_sum = np.ma.array(np.sum(precip_high, axis=0), mask=land_mask.mask)

thresholds = {'1.0': 0., '5.0': 0., '10.0': 0., '20.0': 0., '40.0': 0.,}
thresholds_low = thresholds.copy()
thresholds_mid = thresholds.copy()
thresholds_high = thresholds.copy()

precip_thres = np.empty_like(thresholds)
for t in thresholds.keys():
    _pt = np.where(precip_sum > np.float(t))
    thresholds[t] = (np.float(_pt[0].size) / np.float(land_cells))*100.

precip_thres_low = np.empty_like(thresholds_low)
for t in thresholds_low.keys():
    _pt = np.ma.masked_less_equal(precip_low_sum, np.float(t))
    thresholds_low[t] = (np.float(_pt.count()) / np.float(land_cells))*100.

precip_thres_mid = np.empty_like(thresholds_mid)
for t in thresholds_mid.keys():
    _pt = np.ma.masked_less_equal(precip_mid_sum, np.float(t))
    thresholds_mid[t] = (np.float(_pt.count()) / np.float(land_cells))*100.

precip_thres_high = np.empty_like(thresholds_high)
for t in thresholds_high.keys():
    _pt = np.ma.masked_less_equal(precip_high_sum, np.float(t))
    thresholds_high[t] = (np.float(_pt.count()) / np.float(land_cells))*100.

#ipdb.set_trace()

plt.bar(np.array(thresholds_high.keys(), dtype=np.float), thresholds_high.values(), width=1.2, color='red')
plt.hold(True)
plt.bar(np.array(thresholds_mid.keys(), dtype=np.float), thresholds_mid.values(), width=1.0, color='blue')
plt.bar(np.array(thresholds_low.keys(), dtype=np.float), thresholds_low.values(), color='green')
plt.figure()
plt.imshow(np.flipud(precip_sum)); plt.colorbar()
plt.show()
