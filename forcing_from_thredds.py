#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import netCDF4
from nc_index_by_coordinate import tunnel_fast
from crocus_forcing_nc import CrocusForcing
'''

TODO: add functionality to append data at correct time step, possibly update some time-steps
__author__ = 'kmu'
'''

thredds_url = "http://thredds.met.no/thredds/dodsC/arome25/arome_metcoop_test2_5km_latest.nc"
thredds_file = netCDF4.Dataset(thredds_url, 'r')
latvar = thredds_file.variables['latitude']
lonvar = thredds_file.variables['longitude']

points = {'Hemsedal': [60.86, 8.6],
          'Nordøyan fyr': [64.8, 10.55]
          }
no_points = len(points)
point_index = [tunnel_fast(latvar, lonvar, coord[0], coord[1]) for coord in points.values()]


cnc = CrocusForcing(no_points=no_points) # init Crocus forcing file
cnc.forc_time_step_v[:] = 3600.0


for point in xrange(no_points):
    print(point, point_index[point][0], point_index[point][1])
    cnc.tair_v[:, point] = thredds_file.variables['air_temperature_2m'][:, 0, point_index[point][0], point_index[point][1]]

time_v = thredds_file.variables['time']
cnc.time_v[:] = time_v[:]
cnc.time_v.units = time_v.units

cnc.close()
thredds_file.close()
