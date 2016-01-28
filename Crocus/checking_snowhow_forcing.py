#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import pylab as plt
import netCDF4
import datetime
import numpy as np
"""
Testing the gridded obs-data as forcing data for SnowHow-Crocus modelling.
Author: kmunve

"""

precip_f = r"..\Test\Data\snowhow_pilot\seNorge_v2_0_PREC1h_grid_2015011221_2015011221.nc"
precip_mf = r"..\Test\Data\snowhow_pilot\seNorge_v2_0_PREC1h_grid_*.nc"

temp_f = r"..\Test\Data\snowhow_pilot\seNorge_v2_0_TEMP1h_grid_2015011221.nc"

snowrain_f = r"..\Test\Data\snowhow_pilot\snowrain_only_2015011221.nc"

forc_obs_f = r"..\Test\Data\FORCING_obsgrid.nc"

forc_arome_f = r"..\Test\Data\snowhow_pilot\har25_00_20150112.nc"

X = 45
Y = 1185

precip_nc = netCDF4.Dataset(precip_f, 'r')
temp_nc = netCDF4.Dataset(temp_f, 'r')
snowrain_nc = netCDF4.Dataset(snowrain_f, 'r')
forc_arome_nc = netCDF4.Dataset(forc_arome_f, 'r')
forc_obs_nc = netCDF4.Dataset(forc_obs_f, 'r')

precip_v = precip_nc.variables['precipitation_amount'] ## mm
temp_v = temp_nc.variables['temperature'] ## Celsius
snowrain_v = snowrain_nc.variables['precipitation_amount']



precip_obs_v = forc_obs_nc.variables["Rainf"]

lat_obs = forc_obs_nc.variables["LAT"][:]
lon_obs = forc_obs_nc.variables["LON"][:]
time_obs = forc_obs_nc.variables["time"][:]


time_v = precip_nc.variables['time']
t_p = netCDF4.num2date(time_v[0], time_v.units)
time_v = temp_nc.variables['time']
t_t = netCDF4.num2date(time_v[0], time_v.units)

if t_t == t_p:
    print("Time matches")
else:
    print("Time mismatch")


rainf_arome_v = forc_arome_nc.variables["precipitation_amount_acc"]
rainf_arome = rainf_arome_v[:].squeeze() # kg/m2 = mm

snowf_arome_v = forc_arome_nc.variables["lwe_thickness_of_snowfall_amount_acc"]
snowf_arome = rainf_arome_v[:].squeeze() # kg/m2 = mm

time_arome = netCDF4.num2date(forc_arome_nc.variables["time"][:], forc_arome_nc.variables["time"].units)

precip = precip_v[:].squeeze() #/ 3600.0
snowrain = snowrain_v[:].squeeze()



temp = temp_v[:].squeeze()
rainf = np.ma.masked_where((temp <= 0.5), precip)
snowf = np.ma.masked_where((temp > 0.5), precip)

diff = rainf - snowrain

N_arome = 21

'''
f, (ax_rf, ax_sf, ax_rf_sf) = plt.subplots(1, 3)
ax_rf.imshow(rainf_arome[N_arome, :, :])
ax_rf.set_title("Rain fall (AROME): {0}".format(time_arome[N_arome]))
#plt.colorbar()
ax_sf.imshow(snowf_arome[N_arome, :, :])
ax_sf.set_title("Snow fall (AROME): {0}".format(time_arome[N_arome]))
#plt.colorbar()
ax_rf_sf.imshow(rainf_arome[N_arome, :, :] - snowf_arome[N_arome, :, :])
ax_rf_sf.set_title("Diff. (AROME): {0}".format(time_arome[N_arome]))
'''
f, ([ax_obs, ax_aro], [ax_cobs, ax_caro]) = plt.subplots(2, 2)
im_obs = ax_obs.imshow(precip)
ax_obs.set_title("Precip (obs.grid): {0}".format(t_p))
plt.colorbar(im_obs, cax=ax_cobs, orientation="horizontal")
im_aro = ax_aro.imshow(rainf_arome[21, :, :])
ax_aro.set_title("Precip (AROME): {0}".format(time_arome[21]))
plt.colorbar(im_aro, cax=ax_caro, orientation="horizontal")

plt.figure()
plt.imshow(snowf)
plt.title("Snow fall: {0}".format(t_p))
plt.colorbar()

f, (ax1, ax2, ax3) = plt.subplots(1, 3)
ax1.imshow(rainf)
ax1.set_title("Precip (grid): {0}".format(t_p))
ax2.imshow(snowrain)
ax2.set_title("Precip (conv): {0}".format(t_p))
ax3.imshow(diff)
ax3.set_title("Difference: {0}".format(t_p))

precip_nc_mf = netCDF4.MFDataset(precip_mf)
precip_v_mf = precip_nc_mf.variables['precipitation_amount'] ## mm
precip = precip_v_mf[:].squeeze() / 3600.0
time_v_mf = precip_nc_mf.variables['time']
t_p_mf = netCDF4.num2date(time_v_mf[:], time_v_mf.units)

plt.figure()
plt.plot(t_p_mf, precip[:, Y, X])


plt.show()

