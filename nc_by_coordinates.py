#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylab as plt
import netCDF4
from nc_index_by_coordinate import tunnel_fast

"""
Test to use the tunnel_fast function to extract point data from a netcdf grid.

Author: kmunve

TODO: add info as MD
"""

filename = "http://thredds.met.no/thredds/dodsC/arome25/arome_metcoop_test2_5km_latest.nc"
ncfile = netCDF4.Dataset(filename, 'r')
latvar = ncfile.variables['latitude']
lonvar = ncfile.variables['longitude']

# iy,ix = tunnel_fast(latvar, lonvar, 60.86, 8.6) # Hemsedal
iy,ix = tunnel_fast(latvar, lonvar, 64.8, 10.55) # Nordøyan fyr

print('Closest lat, lon: {0}, {1}; corresponding to indicies: {2}, {3}'.format(latvar[iy,ix], lonvar[iy,ix], ix, iy))

ta2m = ncfile.variables['air_temperature_2m'][9:43, 0, iy, ix] - 273.15

time_v = ncfile.variables['time']
times = netCDF4.num2date(time_v[9:43], time_v.units)

ncfile.close()

plt.plot(times, ta2m)
plt.show()



