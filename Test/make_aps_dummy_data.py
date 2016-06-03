#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from datetime import datetime, timedelta
from netCDF4 import date2num
import numpy as np
from crocus_forcing_nc import CrocusForcing
'''
Create a simple APS data set to test avalanche problem selector.


__author__ = 'kmu'
'''

# Create artificial parameters

# Create the time line
t_start = datetime(2016, 2, 1)
t_stop = datetime(2016, 2, 11)
dt = timedelta(hours=3)
t_units = 'hours since 2016-02-01 00:00:00'
time_arr = np.arange(t_start, t_stop, dt)
time_v = date2num(time_arr.tolist(), t_units)

n = len(time_arr)
n_arr = np.arange(n, dtype=float)

mask_cool1 = np.where(time_arr < datetime(2013, 9, 7))
mask_cold1 = np.where((time_arr >= datetime(2013, 9, 7)) & ((time_arr < datetime(2013, 9, 14))))
mask_cool2 = np.where((time_arr >= datetime(2013, 9, 14)) & ((time_arr < datetime(2013, 10, 1))))
mask_warm1 = np.where((time_arr >= datetime(2013, 10, 1)) & ((time_arr <= datetime(2013, 10, 31))))

mask_snow1 = np.where((time_arr >= datetime(2013, 9, 2)) & ((time_arr <= datetime(2013, 9, 3))))
mask_snow2 = np.where((time_arr >= datetime(2013, 9, 9)) & ((time_arr <= datetime(2013, 9, 10))))
mask_snow3 = np.where((time_arr >= datetime(2013, 9, 16)) & ((time_arr <= datetime(2013, 9, 17))))

tair = np.zeros_like(time_arr, dtype=float)
tair[mask_cool1[0]] = np.array([270.0]*len(mask_cool1[0]), dtype=float)
tair[mask_cold1[0]] = np.array([250.0]*len(mask_cold1[0]), dtype=float)
tair[mask_cool2[0]] = np.array([270.0]*len(mask_cool2[0]), dtype=float)
tair[mask_warm1[0]] = np.array([280.0]*len(mask_warm1[0]), dtype=float)


rainf = np.zeros_like(time_arr, dtype=float)

snowf = np.zeros_like(time_arr, dtype=float)
snowf[mask_snow1[0]] += 1.0e-03
snowf[mask_snow2[0]] += 1.0e-03
snowf[mask_snow3[0]] += 1.0e-03


wind = np.zeros_like(time_arr, dtype=float)
wind += 2.0 # m/s

wind_dir = np.zeros_like(time_arr, dtype=float)

cnc = CrocusForcing(opt_param=['Wind_DIR']) # init Crocus forcing file

# Set some properties
cnc.forc_time_step_v[:] = dt.seconds

cnc.uref_v[:] = 10.0
cnc.zref_v[:] = 2.0
cnc.zs_v[:] = 950.0
cnc.lat_v[:] = 60.0
cnc.lon_v[:] = 10.0

# TODO: use date2num to get the time right
cnc.time_v[:] = time_v
cnc.time_v.units = t_units

# Set the created forcing parameters

#PTH
cnc.tair_v[:, 0] = tair[:]
# Precip
cnc.rain_fall_v[:, 0] = rainf[:]
cnc.snow_fall_v[:, 0] = snowf[:]
# Radiation

# Wind
cnc.wind_v[:, 0] = wind[:]
cnc.wind_dir_v[:, 0] = wind_dir[:]
# Others

#cnc.create_options_nam()
cnc.close()
