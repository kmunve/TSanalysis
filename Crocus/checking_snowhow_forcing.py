#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import pylab as plt
import netCDF4
import datetime

"""
Testing the gridded obs-data as forcing data for SnowHow-Crocus modelling.
Author: kmunve

"""

precip_f = r"..\Test\Data\snowhow_pilot\seNorge_v2_0_PREC1h_grid_2015011206_2015011206.nc"


X = 500
Y = 500

precip_nc = netCDF4.Dataset(precip_f, 'r')
precip_v = precip_nc.variables['precipitation_amount'] ## mm
time_v = precip_nc.variables['time']

precip = precip_v[:].squeeze()
t = netCDF4.num2date(time_v[0], time_v.units)

plt.imshow(precip)
plt.title(t)

plt.show()

