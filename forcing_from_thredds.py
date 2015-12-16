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


def forcing_from_thredds(sites, forc_vars):
    '''

    :param sites: dict with site-name as key and list of [lat, lon] as value.
    .param forc_vars: list of forcing variables to be inserted as forcing
    :return:
    '''
    thredds_url = "http://thredds.met.no/thredds/dodsC/arome25/arome_metcoop_test2_5km_latest.nc"
    thredds_file = netCDF4.Dataset(thredds_url, 'r')
    latvar = thredds_file.variables['latitude']
    lonvar = thredds_file.variables['longitude']

    no_points = len(sites)
    point_index = [tunnel_fast(latvar, lonvar, coord[0], coord[1]) for coord in sites.values()]

    cnc = CrocusForcing(no_points=no_points, source="arome") # init Crocus forcing file
    cnc.forc_time_step_v[:] = 3600.0

    for point in range(no_points):
        for var in forc_vars:
            cnc.insert_arome_var(var, thredds_file.variables)
        #cnc.tair_v[:, point] = thredds_file.variables[cnc.crocus_arome_lut[cnc.tair_v.name]][:, 0, point_index[point][0], point_index[point][1]]

    time_v = thredds_file.variables['time']
    cnc.time_v[:] = time_v[:]
    cnc.time_v.units = time_v.units

    cnc.close()
    thredds_file.close()


if __name__ == "__main__":
    sites = {'Hemsedal': [60.86, 8.6], 'Nordøyan fyr': [64.8, 10.55]}
    forcing_from_thredds(sites, ['Tair'])

