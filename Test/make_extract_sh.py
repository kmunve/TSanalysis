#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = 'kmunve'
__created__ = '2015-09-23'
__version__ = "0.1"
__status__ = "Development"

import os
import netCDF4
import datetime

'''
Wrapper for the fimex command.
Requires fimex to be installed.
'''


def extract_nc_subset(nc_infile, nc_outfile='out.nc', nc_var=[], time_start=None, time_end=None, bounding_box={}, make_script=True):
    '''

    '''
    selected_var = ''
    for var in nc_var:
        selected_var += '--extract.selectVariables={0} '.format(var)

    time_start_strf = datetime.datetime.strftime(time_start, '%Y-%m-%dT%H:%M:%S')
    time_end_strf = datetime.datetime.strftime(time_end, '%Y-%m-%dT%H:%M:%S')

    fimex_command = '''fimex \
--input.file={0} --input.type=netcdf {1}\
--extract.reduceTime.start={2} --extract.reduceTime.end={3} \
--extract.reduceToBoundingBox.south={4} --extract.reduceToBoundingBox.north={5} \
--extract.reduceToBoundingBox.west={6} --extract.reduceToBoundingBox.east={7} \
--output.file={8} --output.type=nc4
    '''.format(nc_infile, selected_var, time_start_strf, time_end_strf, bounding_box['S'], bounding_box['N'], bounding_box['W'], bounding_box['E'], nc_outfile)

    if make_script:
        fid = open('extract_{0}.sh'.format(os.path.splitext(nc_outfile)[0]), 'w')
        fid.write('#!/usr/bin/env bash\n')
        fid.write(fimex_command)
        fid.close()
    else:
        return fimex_command


if __name__ == '__main__':

    # Extract latest data with bounding box around Rauland forecasting region
    url = 'http://thredds.met.no/thredds/dodsC/arome25/arome_metcoop_default2_5km_latest.nc'
    _nc = netCDF4.Dataset(url)
    _t = netCDF4.num2date(_nc.variables['time'][0], _nc.variables['time'].units)
    time_start = _t+datetime.timedelta(hours=6)
    time_end = _t+datetime.timedelta(hours=30)
    _nc.close()

    extract_nc_subset(url,'rauland_f.nc',
        ['time', 'precipitation_amount', 'precipitation_amount_high_estimate', 'precipitation_amount_low_estimate', 'precipitation_amount_middle_estimate', 'land_area_fraction', 'altitude'],
        time_start, time_end, {'S': 59.55, 'N': 60.02, 'W': 7.47, 'E': 9.02})

