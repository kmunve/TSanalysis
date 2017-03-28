#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from datetime import datetime, timedelta

import numpy as np
from netCDF4 import date2num

from Crocus.crocus_forcing_nc import CrocusForcing
'''
Create a forcing data set for SURFEX/Crocus

__author__ = 'kmu'
'''

######################################################################
# LOAD YOUR FONNBU DATA AND ASSIGN IT TO THE VARIABLES CNC.??? BELOW #
######################################################################


# Create the time line (NOT SURE IF YOU NEED THIS)
t_start = datetime(2013, 9, 1, 2)
t_stop = datetime(2013, 10, 31)
dt = timedelta(hours=1)
t_units = 'hours since 2013-09-01 02:00:00'
time_arr = np.arange(t_start, t_stop, dt)
time_v = date2num(time_arr.tolist(), t_units)

n = len(time_arr)

# USE A DUMMY IF YOU DON'T HAVE THE DATA
co2_air = np.zeros_like(time_arr, dtype=float)



cnc = CrocusForcing(opt_param=['Wind_DIR', 'CO2air']) # init Crocus forcing file

# Set some properties
cnc.forc_time_step_v[:] = dt.seconds

# USE CORRECT VALUES FOR FONNBU
cnc.uref_v[:] = 10.0
cnc.zref_v[:] = 2.0
cnc.zs_v[:] = 950.0
cnc.lat_v[:] = 60.0
cnc.lon_v[:] = 10.0

cnc.time_v[:] = time_v
cnc.time_v.units = t_units

# Set the created forcing parameters

#PTH
cnc.q_air_v[:, 0] = q_air[:]
cnc.tair_v[:, 0] = tair[:]
cnc.ps_surf_v[:, 0] = p_surf[:]

cnc.rain_fall_v[:, 0] = rainf[:]
cnc.snow_fall_v[:, 0] = snowf[:]

# Radiation
cnc.dir_sw_down_v[:, 0] = dir_sw_down[:]
cnc.sca_sw_down_v[:, 0] = sca_sw_down[:]
cnc.lw_down_v[:, 0] = lw_down[:]

# Wind
cnc.wind_v[:, 0] = wind[:]
cnc.wind_dir_v[:, 0] = wind_dir[:]

# Others
cnc.co2_air_v[:, 0] = co2_air


cnc.create_options_nam()
cnc.close()
