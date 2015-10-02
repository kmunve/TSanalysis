#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from datetime import datetime, timedelta
from netCDF4 import date2num
import numpy as np
from crocus_forcing_nc import CrocusForcing
'''
Create a simple forcing data set to test snow routines

__author__ = 'kmu'
'''

# Create artificial parameters

t_start = datetime(2015, 12, 01)
t_stop = datetime(2016, 03, 31)
dt = timedelta(hours=1)
t_units = 'hours since 2015-12-01 00:00:00'
time_arr = np.arange(t_start, t_stop, dt)
time_v = date2num(time_arr.tolist(), t_units)

n = len(time_arr)

mask1 = np.where(time_arr > datetime(2016, 02, 31))
tair = np.zeros_like(time_arr, dtype=float)
tair[mask1] += 270.0 # in Kelvin

co2_air = np.zeros_like(time_arr, dtype=float)

p_surf = np.zeros_like(time_arr, dtype=float)
p_surf += 90000.0 # Pa

q_air = np.zeros_like(time_arr, dtype=float)
q_air += 3.0e-03

cnc = CrocusForcing() # init Crocus forcing file

# Set some properties
cnc.forc_time_step_v[:] = dt.seconds
#cnc.aspect_v[:] = 0.0
cnc.uref_v[:] = 2.0
cnc.zref_v[:] = 0.0
cnc.zs_v[:] = 500.0
cnc.lat_v[:] = 60.0
cnc.lon_v[:] = 10.0

# TODO: use date2num to get the time right
cnc.time_v[:] = time_v
cnc.time_v.units = t_units

# Set the created forcing parameters

#PTH
cnc.q_air_v[:, 0] = q_air
cnc.tair_v[:, 0] = tair
cnc.ps_surf_v[:, 0] = p_surf
# Precip
#cnc.rain_fall_v
#cnc.snow_fall_v
# Radiation
#cnc.dir_sw_down_v
#cnc.sca_sw_down_v
#cnc.lw_down_v
# Wind
#cnc.wind_v
# Others
cnc.co2_air_v[:, 0] = co2_air



cnc.close()