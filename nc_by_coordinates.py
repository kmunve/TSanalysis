#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import pylab as plt
import netCDF4
from nc_index_by_coordinate import tunnel_fast
from crocus_forcing_nc import CrocusForcing
from Plotting.meteo_plots import temperature_plot

"""
Test to use the tunnel_fast function to extract point data from a netcdf grid.

Author: kmunve

TODO: add info as MD
"""

filename = "http://thredds.met.no/thredds/dodsC/arome25/arome_metcoop_test2_5km_latest.nc"
ncfile = netCDF4.Dataset(filename, 'r')
latvar = ncfile.variables['latitude']
lonvar = ncfile.variables['longitude']

points = {'Hemsedal': [60.86, 8.6],
          'Nordøyan fyr': [64.8, 10.55]
          }

indicies = [tunnel_fast(latvar, lonvar, coord[0], coord[1]) for coord in points.values()]
#[print(coord[0], coord[1]) for coord in points.values()]
print(indicies, type(indicies[0]), len(points))

# iy,ix = tunnel_fast(latvar, lonvar, 60.86, 8.6) # Hemsedal
# iy,ix = tunnel_fast(latvar, lonvar, 64.8, 10.55) # Nordøyan fyr

#print('Closest lat, lon: {0}, {1}; corresponding to indicies: {2}, {3}'.format(latvar[iy,ix], lonvar[iy,ix], iy, ix))


cnc = CrocusForcing(no_points=len(points))
for point in xrange(len(points)):
    print(point, indicies[point][0], indicies[point][1])
    cnc.tair_v[:, point] = ncfile.variables['air_temperature_2m'][:, 0, indicies[point][0], indicies[point][1]]

time_v = ncfile.variables['time']
cnc.time_v[:] = time_v[:]
cnc.time_v.units = time_v.units

cnc.close()
ncfile.close()

#temperature_plot(ta2m, times)



