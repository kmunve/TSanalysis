#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from datetime import datetime, timedelta
import netCDF4
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
time_v = np.arange(t_start, t_stop, dt)

n = len(time_v)

tair = np.zeros_like(time_v, dtype=float)
tair += 270.0 # in Kelvin

co2_air = np.zeros_like(time_v, dtype=float)


cnc = CrocusForcing() # init Crocus forcing file

# Set some properties
cnc.forc_time_step_v[:] = dt.seconds
cnc.aspect_v[:] = 0.0
cnc.uref_v[:] = 2.0
cnc.zref_v[:] = 0.0
cnc.zs_v[:] = 500.0
cnc.lat_v[:] = 60.0
cnc.lon_v[:] = 10.0

# TODO: use date2num to get the time right
cnc.time_v[:] = time_v
cnc.time_v.units = time_v.units

# Set the created forcing parameters
cnc.tair_v[:, 0] = tair
cnc.co2_air_v[:, 0] = co2_air


cnc.close()