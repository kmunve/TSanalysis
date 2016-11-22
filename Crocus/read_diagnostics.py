#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import pylab as plt
import netCDF4

"""

"""

filename = r"\\unixhome\users\kmu\SURFEX\EXPERIMENTS\nve\ISBA_DIAGNOSTICS.OUT.nc"
ncfile = netCDF4.Dataset(filename, 'r')
var = ncfile.variables['T2M_ISBA']

time_v = ncfile.variables['time']
t = netCDF4.num2date(time_v[:], time_v.units)

plt.plot(t, var[:])
plt.xlabel('Date')
plt.ylabel(var.long_name)

plt.show()

ncfile.close()
