#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import pylab as plt
import netCDF4
import datetime

"""
Comparing forcing data from AROME MetCOOP model and the gridded observational data.

Author: kmunve

"""

arome_f = "../Test/Data/FORCING_arome.nc"
obsgrid_f = "../Test/Data/FORCING_obsgrid.nc"


#N = 35360
N = 64197

arome_nc = netCDF4.Dataset(arome_f, 'r')
obsgrid_nc = netCDF4.Dataset(obsgrid_f, 'r')


###
# AROME #
###

a_lat_v = arome_nc.variables['LAT']
a_lon_v = arome_nc.variables['LON']

a_masl_v = arome_nc.variables['ZS']

a_ta_v = arome_nc.variables['Tair']
a_rr_v = arome_nc.variables['Rainf']
a_sf_v = arome_nc.variables['Snowf']
a_time_v = arome_nc.variables['time']

a_t = a_time_v[:]#netCDF4.num2date(a_time_v[:], a_time_v.units)
a_ta = a_ta_v[:, N]
a_rr = a_rr_v[:, N]
a_sf = a_sf_v[:, N]


####
# OBSGRID
####


o_lat_v = obsgrid_nc.variables['LAT']
o_lon_v = obsgrid_nc.variables['LON']

o_masl_v = obsgrid_nc.variables['ZS']

o_ta_v = obsgrid_nc.variables['Tair']
o_rr_v = obsgrid_nc.variables['Rainf']
o_sf_v = obsgrid_nc.variables['Snowf']
o_time_v = obsgrid_nc.variables['time']

o_t = o_time_v[:]#netCDF4.num2date(o_time_v[:], o_time_v.units)
o_ta = o_ta_v[:, N]
o_rr = o_rr_v[:, N]
o_sf = o_sf_v[:, N]

#t_width = datetime.timedelta(minutes=30)
width = 0.25

f, axarr = plt.subplots(3, sharex=True)
plt.hold(True)
axarr[0].axhline(273.65, color='k', linestyle="--")
axarr[0].plot(o_t, o_ta, color='r')
axarr[0].plot(a_t, a_ta, color='b')
axarr[0].set_title("OBSGRID coords: {0}, {1}\nAROME coords: {2}, {3}".format(o_lat_v[N], o_lon_v[N], a_lat_v[N], a_lon_v[N]))
axarr[0].set_ylabel("Temperature")

axarr[1].bar(o_t+width, o_rr, width=width, color='r')
axarr[1].bar(a_t, a_rr, width=width, color='b')
axarr[1].set_ylabel("Rainfall rate")

axarr[2].bar(o_t+width, o_sf, width=width, color='r')
axarr[2].bar(a_t, a_sf, width=width, color='b')
axarr[2].set_ylabel("Snowfall rate")
plt.show()
