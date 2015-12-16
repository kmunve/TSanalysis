#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from netCDF4 import Dataset, num2date
from string import Template
from datetime import datetime
'''
Create a forcing netcdf file for the snow pack model Crocus.
'''


class CrocusForcing:

    def __init__(self, no_points=1, filename=None, opt_param=[], source="Unspecified"):
        '''
        TODO: add a plotting routine to view all parameters.


        :param no_points: the number of points/stations that should be modeled
        :param filename: if given an existing file will be opened to append data
        :param opt_param: list containing optional parameters that can be set
        These are:
        - relative humidity (HUMREL)
        - nebulosity (NEB)
        - wind direction (Wind_DIR)

        :param source: Unknown, eklima or arome - TODO: make an Enum
        :return: creates FORCING.nc
        '''

        self._set_crocus_arome_lut()
        self._set_crocus_eklima_lut()

        if filename is None:
            # Set general parameters
            self.fill_value = -9999999.0

            # create a file (Dataset object, also the root group).
            self.rootgrp = Dataset('FORCING.nc', 'w', format='NETCDF3_CLASSIC') # TODO: should be changed to NETCDF4 once Surfex8 is ready

            ##############
            # Dimensions #
            ##############
            self.time_dim = self.rootgrp.createDimension('time', None)
            self.number_of_points_dim = self.rootgrp.createDimension('Number_of_points', no_points)

            #####################
            # Global attributes #
            #####################

            self.rootgrp.description = "SURFEX/Crocus forcing file"
            self.rootgrp.history = "Created " + datetime.now().isoformat()
            if source == "arome":
                self.rootgrp.source = "AROME MetCoop - NWP model"
            elif source == "eklima":
                self.rootgrp.source = "www.eklima.no - wsKlima API"
            else:
                self.rootgrp.source = "unspecified"

            #############
            # Variables #
            #############

            ###########
            # Scalars #
            ###########
            self.forc_time_step_v = self.rootgrp.createVariable('FRC_TIME_STP','f8',fill_value=self.fill_value)
            self.forc_time_step_v.units = 's'
            self.forc_time_step_v.long_name = 'Forcing_Time_Step'

            ######
            # 1D #
            ######
            self.time_v = self.rootgrp.createVariable('time', 'f8', ('time',), fill_value=self.fill_value)
            # depends on FORC_TIME_STP units
            self.time_v.units = 'hours/seconds since '
            self.time_v.long_name = 'time'
            if source == "arome":
                self.time_v.derived_from_arome = self.crocus_arome_lut['time']
            elif source == "eklima":
                self.time_v.derived_from_eklima = self.crocus_eklima_lut['time']

            self.lat_v = self.rootgrp.createVariable('LAT', 'f8', ('Number_of_points',), fill_value=self.fill_value)
            self.lat_v.units = 'degrees_north'
            self.lat_v.long_name = 'latitude'
            if source == "arome":
                self.lat_v.derived_from_arome = self.crocus_arome_lut['LAT']
            elif source == "eklima":
                self.lat_v.derived_from_eklima = self.crocus_eklima_lut['LAT']

            self.lon_v = self.rootgrp.createVariable('LON', 'f8', ('Number_of_points',), fill_value=self.fill_value)
            self.lon_v.units = 'degrees_east'
            self.lon_v.long_name = 'longitude'
            if source == "arome":
                self.lon_v.derived_from_arome = self.crocus_arome_lut['LON']
            elif source == "eklima":
                self.lon_v.derived_from_eklima = self.crocus_eklima_lut['LON']

            if 'aspect' in opt_param:
                self.aspect_v = self.rootgrp.createVariable('aspect', 'f8', ('Number_of_points'),fill_value=self.fill_value)
                self.aspect_v.units = 'degrees from north'
                self.aspect_v.long_name = 'slope aspect'

            if 'slope' in opt_param:
                self.slope_v = self.rootgrp.createVariable('slope','f8',('Number_of_points',),fill_value=self.fill_value)
                self.slope_v.units = 'degrees from horizontal'
                self.slope_v.long_name = 'slope angle'

            self.uref_v = self.rootgrp.createVariable('UREF','f8',('Number_of_points',),fill_value=self.fill_value)
            self.uref_v.units = 'm'
            self.uref_v.long_name = 'Reference_Height_for_Wind'

            self.zref_v = self.rootgrp.createVariable('ZREF','f8',('Number_of_points',),fill_value=self.fill_value)
            self.zref_v.units = 'm'
            self.zref_v.long_name = 'Reference_Height'

            self.zs_v = self.rootgrp.createVariable('ZS','f8',('Number_of_points',),fill_value=self.fill_value)
            self.zs_v.units = 'm'
            self.zs_v.long_name = 'altitude'
            if source == "arome":
                self.zs_v.derived_from_arome = self.crocus_arome_lut['ZS']
            elif source == "eklima":
                self.zs_v.derived_from_eklima = self.crocus_eklima_lut['ZS']

            ######
            # 2D #
            ######
            if 'CO2air' in opt_param:
                self.co2_air_v = self.rootgrp.createVariable('CO2air','f8',('time', 'Number_of_points',),fill_value=self.fill_value)
                self.co2_air_v.units = 'kg/m3'
                self.co2_air_v.long_name = 'Near_Surface_CO2_Concentration'
                if source == "arome":
                    self.co2_air_v.derived_from_arome = self.crocus_arome_lut['CO2air']
                elif source == "eklima":
                    self.co2_air_v.derived_from_eklima = self.crocus_eklima_lut['CO2air']

            self.dir_sw_down_v = self.rootgrp.createVariable('DIR_SWdown','f8',('time', 'Number_of_points',),fill_value=self.fill_value)
            self.dir_sw_down_v.units = 'W/m2'
            self.dir_sw_down_v.long_name = 'Surface_Indicent_Direct_Shortwave_Radiation'
            if source == "arome":
                self.dir_sw_down_v.derived_from_arome = self.crocus_arome_lut['DIR_SWdown']
            elif source == "eklima":
                self.dir_sw_down_v.derived_from_eklima = self.crocus_eklima_lut['DIR_SWdown']

            if 'HUMREL' in opt_param:
                self.hum_rel_v = self.rootgrp.createVariable('HUMREL','f8',('time', 'Number_of_points',),fill_value=self.fill_value)
                self.hum_rel_v.units = '%'
                self.hum_rel_v.long_name = 'Relative Humidity'
                if source == "arome":
                    self.hum_rel_v.derived_from_arome = self.crocus_arome_lut['HUMREL']
                elif source == "eklima":
                    self.hum_rel_v.derived_from_eklima = self.crocus_eklima_lut['HUMREL']

            self.lw_down_v = self.rootgrp.createVariable('LWdown','f8',('time', 'Number_of_points',),fill_value=self.fill_value)
            self.lw_down_v.units = 'W/m2'
            self.lw_down_v.long_name = 'Surface_Incident_Longwave_Radiation'
            if source == "arome":
                self.lw_down_v.derived_from_arome = self.crocus_arome_lut['LWdown']
            elif source == "eklima":
                self.lw_down_v.derived_from_eklima = self.crocus_eklima_lut['LWdown']

            if 'NEB' in opt_param:
                self.neb_v = self.rootgrp.createVariable('NEB','f8',('time', 'Number_of_points',),fill_value=self.fill_value)
                self.neb_v.units = 'between 0 and 1'
                self.neb_v.long_name = 'Nebulosity'
                if source == "arome":
                    self.neb_v.derived_from_arome = self.crocus_arome_lut['NEB']
                elif source == "eklima":
                    self.neb_v.derived_from_eklima = self.crocus_eklima_lut['NEB']

            self.ps_surf_v = self.rootgrp.createVariable('PSurf','f8',('time', 'Number_of_points',),fill_value=self.fill_value)
            self.ps_surf_v.units = 'Pa'
            self.ps_surf_v.long_name = 'Surface_Pressure'
            if source == "arome":
                self.ps_surf_v.derived_from_arome = self.crocus_arome_lut['PSurf']
            elif source == "eklima":
                self.ps_surf_v.derived_from_eklima = self.crocus_eklima_lut['PSurf']

            self.q_air_v = self.rootgrp.createVariable('Qair','f8',('time', 'Number_of_points',),fill_value=self.fill_value)
            self.q_air_v.units = 'Kg/Kg'
            self.q_air_v.long_name = 'Near_Surface_Specific_Humidity'
            if source == "arome":
                self.q_air_v.derived_from_arome = self.crocus_arome_lut['Qair']
            elif source == "eklima":
                self.q_air_v.derived_from_eklima = self.crocus_eklima_lut['Qair']

            self.rain_fall_v = self.rootgrp.createVariable('Rainf','f8',('time', 'Number_of_points',),fill_value=self.fill_value)
            self.rain_fall_v.units = 'kg/m2/s'
            self.rain_fall_v.long_name = 'Rainfall_Rate'
            if source == "arome":
                self.rain_fall_v.derived_from_arome = self.crocus_arome_lut['Rainf']
            elif source == "eklima":
                self.rain_fall_v.derived_from_eklima = self.crocus_eklima_lut['Rainf']

            self.sca_sw_down_v = self.rootgrp.createVariable('SCA_SWdown','f8',('time', 'Number_of_points',),fill_value=self.fill_value)
            self.sca_sw_down_v.units = 'W/m2'
            self.sca_sw_down_v.long_name = 'Surface_Incident_Diffuse_Shortwave_Radiation'
            if source == "arome":
                self.sca_sw_down_v.derived_from_arome = self.crocus_arome_lut['SCA_SWdown']
            elif source == "eklima":
                self.sca_sw_down_v.derived_from_eklima = self.crocus_eklima_lut['SCA_SWdown']

            self.snow_fall_v = self.rootgrp.createVariable('Snowf','f8',('time', 'Number_of_points',),fill_value=self.fill_value)
            self.snow_fall_v.units = 'kg/m2/s'
            self.snow_fall_v.long_name = 'Snowfall_Rate'
            if source == "arome":
                self.snow_fall_v.derived_from_arome = self.crocus_arome_lut['Snowf']
            elif source == "eklima":
                self.snow_fall_v.derived_from_eklima = self.crocus_eklima_lut['Snowf']

            self.tair_v = self.rootgrp.createVariable('Tair','f8',('time', 'Number_of_points',),fill_value=self.fill_value)
            self.tair_v.units = 'K'
            self.tair_v.long_name = 'Near_Surface_Air_Temperature'
            self.tair_v.derived_from_arome = 'air_temperature_2m'
            if source == "arome":
                self.tair_v.derived_from_arome = self.crocus_arome_lut['Tair']
            elif source == "eklima":
                self.tair_v.derived_from_eklima = self.crocus_eklima_lut['Tair']

            self.wind_v = self.rootgrp.createVariable('Wind','f8',('time', 'Number_of_points',),fill_value=self.fill_value)
            self.wind_v.units = 'm/s'
            self.wind_v.long_name = 'Wind_Speed'
            if source == "arome":
                self.wind_v.derived_from_arome = self.crocus_arome_lut['Wind']
            elif source == "eklima":
                self.wind_v.derived_from_eklima = self.crocus_eklima_lut['Wind']

            if 'Wind_DIR' in opt_param:
                self.wind_dir_v = self.rootgrp.createVariable('Wind_DIR','f8',('time', 'Number_of_points',),fill_value=self.fill_value)
                self.wind_dir_v.units = 'deg'
                self.wind_dir_v.long_name = 'Wind_Direction'
                if source == "arome":
                    self.wind_dir_v.derived_from_arome = self.crocus_arome_lut['Wind_DIR']
                elif source == "eklima":
                    self.wind_dir_v.derived_from_eklima = self.crocus_eklima_lut['Wind_DIR']

        else:
            self.rootgrp = Dataset(filename, 'a')


    def close(self):
        """
        Closes netCDF file after writing.
        """
        self.rootgrp.close()

    def set_variable(self, var):
        pass

    def _set_crocus_arome_lut(self):
        # TODO: cross-check units
        # TODO: cross-check time conversions and time reference
        # Look-up table between Crocus FORCING.nc and arome_metcoop*test*.nc
        self.crocus_arome_lut = {'time': 'time', # seconds since : seconds since
                                'LAT': 'latitude', # degrees_north : degrees_north - ok
                                'LON': 'longitude', # degrees_east : degrees_east - ok
                                'PSurf': 'surface_air_pressure', # Pa : Pa - ok
                                'Tair': 'air_temperature_2m', # : K : K - ok
                                'HUMREL': 'relative_humidity_2m', # % : 1
                                'LWdown': 'integral_of_surface_downwelling_longwave_flux_in_air_wrt_time', # W/m2 : W s/m^2
                                'NEB': '', # 0-1 :
                                'Qair': 'specific_humidity_ml', # Kg/Kg : Kg/Kg - need to address lowest model level !?
                                'Rainf': 'rainfall_amount_pl', # kg/m2/s : kg/m2 - need to address PL and rate
                                'SCA_SWdown': '', # W/m2 :
                                'DIR_SWdown': 'integral_of_surface_downwelling_shortwave_flux_in_air_wrt_time', # W/m2 : W s/m2 - need to adjust for rate
                                'CO2_air': '', # kg/m3 :
                                'Snowf': 'snowfall_amount_pl', # kg/m2/s : kg/m2 - need to address PL and rate (divide by 3600 if hourly)
                                'theorSW': '', # W/m2 :
                                'UREF': '', # m :
                                'Wind': '', # m/s :
                                'Wind_DIR': '', # deg :
                                'aspect': '', # degrees from north :
                                'slope': '', # degrees from horizontal :
                                'ZREF': '', # m :
                                'ZS': '' # m :
                                }

    def _set_crocus_eklima_lut(self):
        # TODO: cross-check units
        # TODO: cross-check time conversions and time reference
        # TODO: conversion to correct units and rates where necessary
        # Look-up table between Crocus FORCING.nc and eklima getMetData return
        self.crocus_eklima_lut = {'time': 'time', # seconds since : seconds since
                                'LAT': 'latDec', # degrees_north : degrees_north - ok
                                'LON': 'lonDec', # degrees_east : degrees_east - ok
                                'Psurf': '', # Pa :
                                'Tair': 'TA', # : K : C
                                'HUMREL': '', # % :
                                'LWdown': '', # W/m2 :
                                'NEB': '', # 0-1 :
                                'Qair': '', # Kg/Kg :
                                'Rainf': 'RR_1', # kg/m2/s : mm
                                'SCA_SWdown': '', # W/m2 :
                                'DIR_SWdown': '', # W/m2 :
                                'CO2_air': '', # kg/m3 :
                                'Snowf': '', # kg/m2/s :
                                'theorSW': '', # W/m2 :
                                'UREF': '', # m : m should be 10 m
                                'Wind': 'FF', # m/s : m/s
                                'Wind_DIR': 'DD', # deg : deg
                                'aspect': '', # degrees from north : -
                                'slope': '', # degrees from horizontal : -
                                'ZREF': '', # m : m from station_props
                                'ZS': '' # m :
                                }

    def insert_arome_var(self, var_name, arome_variables):
        # TODO: can I pass a values to the function in a dict? http://code.activestate.com/recipes/181064/
        self._arome_converter = {'Rainf': self._insert_arome_rainf()}
        if var_name == 'Rainf':
            pass
        else:
            pass


    def _insert_arome_rainf(self):


    def insert_eklima_station(self, i, station, data):
        '''

        :param i: number of point in the Forcing file
        :param station: dict['stnr'] returned from wsklima_parser.parse_get_stations_properties()
        :param data: dict['stnr'] returned from wsklima_parser.parse_get_data()
        :return:
        '''

        # Set time properties - only once not for each station
        self.forc_time_step_v[:] = dt.seconds
        # TODO: use date2num to get the time right
        self.time_v[i] = time_v
        self.time_v.units = t_units

        # Set station properties
        # self.aspect_v[:] = 0.0
        self.uref_v[i] = 10.0
        self.zref_v[i] = 2.0
        self.zs_v[i] = station['amsl']
        self.lat_v[i] = station['latDec']
        self.lon_v[i] = station['lonDec']

        for key in data.keys():
            if key in self.crocus_eklima_lut.values():
                self._insert_eklima_data(i, key, data[key])
        # Set the created forcing parameters
        # PTH
        self.q_air_v[:, i] = q_air[:]
        self.tair_v[:, i] = tair[:]
        self.ps_surf_v[:, i] = p_surf[:]
        # Precip
        self.rain_fall_v[:, i] = rainf[:]
        self.snow_fall_v[:, i] = snowf[:]
        # Raadiation
        self.dir_sw_down_v[:, i] = dir_sw_down[:]
        self.sca_sw_down_v[:, i] = sca_sw_down[:]
        self.lw_down_v[:, i] = lw_down[:]
        # Wind
        self.wind_v[:, i] = wind[:]
        self.wind_dir_v[:, i] = wind_dir[:]
        # Others
        self.co2_air_v[:, i] = co2_air


    def _insert_eklima_data(self, i, key, data):
        # TODO: need to make sure that it is inserted at the correct time!!!
        if key== 'TA':
            self.tair_v[:, i] = data[:]


    def _convert_eklima_precip(self, RR_1, TA):
        '''

        :param RR_1: amount of rain within last hour in mm from eklima station
        :param TA: 2m air temperature in C from eklima station
        :return: sets self.Rainf or self.Snowf in kg/m2/s
        '''
        if TA >= 0.5:
            self.Snowf = 0.0
            self.Rainf = 1000.0 * RR_1 / 3600.0
        else:
            self.Rainf = 0.0
            self.Snowf = 1000.0 * RR_1 / 3600.0


    def create_options_nam(self):
        '''

        * Returns: OPTIONs.nam file

        TODO: adapt for multiple points
        TODO: add option to insert an existing snow pack - maybe in a different function as optional


        &NAM_PREP_ISBA_SNOW
            CSNOW
            NSNOW_LAYER
            CFILE_SNOW
            CTYPE_SNOW
            CFILEPGD_SNOW
            CTYPEPGD_SNOW
            LSNOW_IDEAL
            lSNOW_FRAC_TOT
            XWSNOW
            XZSNOW - NEW IN v8
            XTSNOW
            XLWCSNOW - NEW IN v8
            XRSNOW
            XASNOW
            XSG1SNOW
            XSG2SNOW
            XHISTSNOW
            XAGESNOW

        '''
        option_file = open('OPTIONS.nam', 'w')
        option_template = Template(open('./Test/Data/OPTIONS.nam.tpl', 'r').read())
        # Read the lines from the template, substitute the values, and write to the new config file
        _date = self.time_v.units.split(' ')[2]
        _time = self.time_v.units.split(' ')[3]

        subst = dict(LAT=str(self.lat_v[0]),
                     LON=str(self.lon_v[0]),
                     NO_POINTS=1,
                     ZS=950,
                     YEAR=_date.split('-')[0],
                     MONTH=_date.split('-')[1],
                     DAY=_date.split('-')[2],
                     XTIME=float(_time.split(':')[0])*3600.,
                     )

        _sub_str = option_template.substitute(subst)
        option_file.write(_sub_str)

        # Close the files
        option_file.close()
        #option_template.close()


    def init_from_file(self, filename):
        """
        TODO: adjust or remove
        """
        # create a file (Dataset object, also the root group).
        f = Dataset(filename, mode='r')
        print(f.file_format)
        print(f.dimensions['Number_of_points'])
        print(f.dimensions['time'])
        print(f.variables.keys())
        for var in f.ncattrs():
            print(var, getattr(f, var))
        print(f.variables['Wind'])
        print(f.variables['Wind'].units)
        f.variables['Wind'][:] = []
        print(f.variables['Wind'])
        f.close()

def init_forcing_nc(no_points=1):
    """
    Input no_points: Number of points used in the model grid

    *_dim* indicates a netcdf-dimension
    *_v* indicates a netcdf-variable
    """
    # create a file (Dataset object, also the root group).
    rootgrp = Dataset('FORCING.nc', 'w', format='NETCDF3_CLASSIC')
    print(rootgrp.file_format)

    ##############
    # Dimensions #
    ##############
    time_dim = rootgrp.createDimension('time', None)
    number_of_points_dim = rootgrp.createDimension('Number_of_points', no_points)

    print(rootgrp.dimensions)

    print(time_dim.isunlimited())
    print(number_of_points_dim.isunlimited())

    #############
    # Variables #
    #############

    ###########
    # Scalars #
    ###########
    forc_time_step_v = rootgrp.createVariable('FRC_TIME_STP','f8')
    forc_time_step_v.units = 's'
    forc_time_step_v.long_name = 'Forcing_Time_Step'

    ######
    # 1D #
    ######
    time_v = rootgrp.createVariable('time','f8',('time',))
    # depends on FORC_TIME_STP units
    time_v.units = 'hours/seconds since '
    time_v.long_name = 'time'

    lat_v = rootgrp.createVariable('LAT','f8',('Number_of_points',))
    lat_v.units = 'degrees_north'
    lat_v.long_name = 'latitude'

    lon_v = rootgrp.createVariable('LON','f8',('Number_of_points',))
    lon_v.units = 'degrees_east'
    lon_v.long_name = 'longitude'

    aspect_v = rootgrp.createVariable('aspect', 'f8', ('Number_of_points'))
    aspect_v.units = 'degrees from north'
    aspect_v.long_name = 'slope aspect'

    slope_v = rootgrp.createVariable('slope','f8',('Number_of_points',))
    slope_v.units = 'degrees from horizontal'
    slope_v.long_name = 'slope angle'

    uref_v = rootgrp.createVariable('UREF','f8',('Number_of_points',))
    uref_v.units = 'm'
    uref_v.long_name = 'Reference_Height_for_Wind'

    zref_v = rootgrp.createVariable('ZREF','f8',('Number_of_points',))
    zref_v.units = 'm'
    zref_v.long_name = 'Reference_Height'

    zs_v = rootgrp.createVariable('ZS','f8',('Number_of_points',))
    zs_v.units = 'm'
    zs_v.long_name = 'altitude'

    ######
    # 2D #
    ######
    co2_air_v = rootgrp.createVariable('CO2air','f8',('time', 'Number_of_points',))
    co2_air_v.units = 'kg/m3'
    co2_air_v.long_name = 'Near_Surface_CO2_Concentration'

    dir_sw_down_v = rootgrp.createVariable('DIR_SWdown','f8',('Number_of_points',))
    dir_sw_down_v.units = 'W/m2'
    dir_sw_down_v.long_name = 'Surface_Indicent_Direct_Shortwave_Radiation'

    hum_rel_v = rootgrp.createVariable('HUMREL','f8',('time', 'Number_of_points',))
    hum_rel_v.units = '%'
    hum_rel_v.long_name = 'Relative Humidity'

    lw_down_v = rootgrp.createVariable('LWdown','f8',('time', 'Number_of_points',))
    lw_down_v.units = 'W/m2'
    lw_down_v.long_name = 'Surface_Incident_Longwave_Radiation'

    neb_v = rootgrp.createVariable('NEB','f8',('time', 'Number_of_points',))
    neb_v.units = 'between 0 and 1'
    neb_v.long_name = 'Nebulosity'

    ps_surf_v = rootgrp.createVariable('PSurf','f8',('time', 'Number_of_points',))
    ps_surf_v.units = 'Pa'
    ps_surf_v.long_name = 'Surface_Pressure'

    q_air_v = rootgrp.createVariable('Qair','f8',('time', 'Number_of_points',))
    q_air_v.units = 'Kg/Kg'
    q_air_v.long_name = 'Near_Surface_Specific_Humidity'

    rain_fall_v = rootgrp.createVariable('Rainf','f8',('time', 'Number_of_points',))
    rain_fall_v.units = 'kg/m2/s'
    rain_fall_v.long_name = 'Rainfall_Rate'

    sca_sw_down_v = rootgrp.createVariable('SCA_SWdown','f8',('time', 'Number_of_points',))
    sca_sw_down_v.units = 'W/m2'
    sca_sw_down_v.long_name = 'Surface_Incident_Diffuse_Shortwave_Radiation'

    snow_fall_v = rootgrp.createVariable('Snowf','f8',('time', 'Number_of_points',))
    snow_fall_v.units = 'kg/m2/s'
    snow_fall_v.long_name = 'Snowfall_Rate'

    tair_v = rootgrp.createVariable('Tair','f8',('time', 'Number_of_points',))
    tair_v.units = 'K'
    tair_v.long_name = 'Near_Surface_Air_Temperature'

    wind_v = rootgrp.createVariable('Wind','f8',('time', 'Number_of_points',))
    wind_v.units = 'm/s'
    wind_v.long_name = 'Wind_Speed'

    wind_dir_v = rootgrp.createVariable('Wind_DIR','f8',('time', 'Number_of_points',))
    wind_dir_v.units = 'deg'
    wind_dir_v.long_name = 'Wind_Direction'

    rootgrp.close()




def populate_forcing_nc(df):
    """
    Add values to the empty netcdf file from the pandas DataFrame "df"
    """
    id_dict = {'TAM': 'Tair'}

    # Create new and empty FORCING.nc file with correct number of points
    init_forcing_nc()
    # Open FORCING.nc file, r+ ensures that it exists
    nc = Dataset('FORCING.nc', 'r+', format='NETCDF3_CLASSIC')


    # Fill the time variable
    nc.variables['time'].units, nc.variables['time'][:] = get_nc_time(df.index)
    print(nc.variables['time'])

    for col in df.columns:
        if col in id_dict.keys():
            print(df[col], nc.variables[id_dict[col]])
            nc.variables[id_dict[col]] = df[col]
            print(nc.variables[id_dict[col]])

    nc.close()

def get_nc_time(df_index):

    #
    print(df_index[0])
    tinterval = df_index[1]-df_index[0]
    print(tinterval)
    # find out if it is hours or seconds that are most convinient
    tstart = df_index[0]
    return unit_str, time_array



def test_tutorial():
# 2 unlimited dimensions.
#temp = rootgrp.createVariable('temp','f4',('time','level','lat','lon',))
# this makes the compression 'lossy' (preserving a precision of 1/1000)
# try it and see how much smaller the file gets.
    temp = rootgrp.createVariable('temp','f4',('time','level','lat','lon',),least_significant_digit=3)
# attributes.
    import time
    rootgrp.description = 'bogus example script'
    rootgrp.history = 'Created ' + time.ctime(time.time())
    rootgrp.source = 'netCDF4 python module tutorial'
    latitudes.units = 'degrees north'
    longitudes.units = 'degrees east'
    levels.units = 'hPa'
    temp.units = 'K'
    times.units = 'hours since 0001-01-01 00:00:00.0'
    times.calendar = 'gregorian'
    for name in rootgrp.ncattrs():
        print('Global attr', name, '=', getattr(rootgrp,name))
    print(rootgrp)
    print(rootgrp.__dict__)
    print(rootgrp.variables)
    print(rootgrp.variables['temp'])
    import numpy
# no unlimited dimension, just assign to slice.
    lats = numpy.arange(-90,91,2.5)
    lons = numpy.arange(-180,180,2.5)
    latitudes[:] = lats
    longitudes[:] = lons
    print('latitudes =\n',latitudes[:])
    print('longitudes =\n',longitudes[:])
# append along two unlimited dimensions by assigning to slice.
    nlats = len(rootgrp.dimensions['lat'])
    nlons = len(rootgrp.dimensions['lon'])
    print('temp shape before adding data = ',temp.shape)
    from numpy.random.mtrand import uniform # random number generator.
    temp[0:5,0:10,:,:] = uniform(size=(5,10,nlats,nlons))
    print('temp shape after adding data = ',temp.shape)
# levels have grown, but no values yet assigned.
    print('levels shape after adding pressure data = ',levels.shape)
# assign values to levels dimension variable.
    levels[:] = [1000.,850.,700.,500.,300.,250.,200.,150.,100.,50.]
# fancy slicing
    tempdat = temp[::2, [1,3,6], lats>0, lons>0]
    print('shape of fancy temp slice = ',tempdat.shape)
    print(temp[0, 0, [0,1,2,3], [0,1,2,3]].shape)
# fill in times.
    from datetime import datetime, timedelta
    from netCDF4 import num2date, date2num, date2index
    dates = [datetime(2001,3,1)+n*timedelta(hours=12) for n in range(temp.shape[0])]
    times[:] = date2num(dates,units=times.units,calendar=times.calendar)
    print('time values (in units %s): ' % times.units+'\\n',times[:])
    dates = num2date(times[:],units=times.units,calendar=times.calendar)
    print('dates corresponding to time values:\\n',dates)
    rootgrp.close()
# create a series of netCDF files with a variable sharing
# the same unlimited dimension.
    for nfile in range(10):
        f = Dataset('mftest'+repr(nfile)+'.nc','w',format='NETCDF4_CLASSIC')
        f.createDimension('x',None)
        x = f.createVariable('x','i',('x',))
        x[0:10] = numpy.arange(nfile*10,10*(nfile+1))
    f.close()
# now read all those files in at once, in one Dataset.
    from netCDF4 import MFDataset
    f = MFDataset('mftest*nc')
    print(f.variables['x'][:])
# example showing how to save numpy complex arrays using compound types.
    f = Dataset('complex.nc','w')
    size = 3 # length of 1-d complex array
# create sample complex data.
    datac = numpy.exp(1j*(1.+numpy.linspace(0, numpy.pi, size)))
    print(datac.dtype)
# create complex128 compound data type.
    complex128 = numpy.dtype([('real',numpy.float64),('imag',numpy.float64)])
    complex128_t = f.createCompoundType(complex128,'complex128')
# create a variable with this data type, write some data to it.
    f.createDimension('x_dim',None)
    v = f.createVariable('cmplx_var',complex128_t,'x_dim')
    data = numpy.empty(size,complex128) # numpy structured array
    data['real'] = datac.real; data['imag'] = datac.imag
    v[:] = data
# close and reopen the file, check the contents.
    f.close()
    f = Dataset('complex.nc')
    print(f)
    print(f.variables['cmplx_var'])
    print(f.cmptypes)
    print(f.cmptypes['complex128'])
    v = f.variables['cmplx_var']
    print(v.shape)
    datain = v[:] # read in all the data into a numpy structured array
# create an empty numpy complex array
    datac2 = numpy.empty(datain.shape,numpy.complex128)
# .. fill it with contents of structured array.
    datac2.real = datain['real']
    datac2.imag = datain['imag']
    print(datac.dtype,datac)
    print(datac2.dtype,datac2)
# more complex compound type example.
    from netCDF4 import chartostring, stringtoarr
    f = Dataset('compound_example.nc','w') # create a new dataset.
# create an unlimited dimension call 'station'
    f.createDimension('station',None)
# define a compound data type (can contain arrays, or nested compound types).
    NUMCHARS = 80 # number of characters to use in fixed-length strings.
    winddtype = numpy.dtype([('speed','f4'),('direction','i4')])
    statdtype = numpy.dtype([('latitude', 'f4'), ('longitude', 'f4'),
                             ('surface_wind',winddtype),
                             ('temp_sounding','f4',10),('press_sounding','i4',10),
                             ('location_name','S1',NUMCHARS)])
# use this data type definitions to create a compound data types
# called using the createCompoundType Dataset method.
# create a compound type for vector wind which will be nested inside
# the station data type. This must be done first!
    wind_data_t = f.createCompoundType(winddtype,'wind_data')
# now that wind_data_t is defined, create the station data type.
    station_data_t = f.createCompoundType(statdtype,'station_data')
# create nested compound data types to hold the units variable attribute.
    winddtype_units = numpy.dtype([('speed','S1',NUMCHARS),('direction','S1',NUMCHARS)])
    statdtype_units = numpy.dtype([('latitude', 'S1',NUMCHARS), ('longitude', 'S1',NUMCHARS),
                                   ('surface_wind',winddtype_units),
                                   ('temp_sounding','S1',NUMCHARS),
                                   ('location_name','S1',NUMCHARS),
                                   ('press_sounding','S1',NUMCHARS)])
# create the wind_data_units type first, since it will nested inside
# the station_data_units data type.
    wind_data_units_t = f.createCompoundType(winddtype_units,'wind_data_units')
    station_data_units_t =\
        f.createCompoundType(statdtype_units,'station_data_units')
# create a variable of of type 'station_data_t'
    statdat = f.createVariable('station_obs', station_data_t, ('station',))
# create a numpy structured array, assign data to it.
    data = numpy.empty(1,station_data_t)
    data['latitude'] = 40.
    data['longitude'] = -105.
    data['surface_wind']['speed'] = 12.5
    data['surface_wind']['direction'] = 270
    data['temp_sounding'] = (280.3,272.,270.,269.,266.,258.,254.1,250.,245.5,240.)
    data['press_sounding'] = range(800,300,-50)
    # variable-length string datatypes are not supported inside compound types, so
# to store strings in a compound data type, each string must be
# stored as fixed-size (in this case 80) array of characters.
    data['location_name'] = stringtoarr('Boulder, Colorado, USA',NUMCHARS)
# assign structured array to variable slice.
    statdat[0] = data
# or just assign a tuple of values to variable slice
# (will automatically be converted to a structured array).
    statdat[1] = (40.78,-73.99,(-12.5,90),
                  (290.2,282.5,279.,277.9,276.,266.,264.1,260.,255.5,243.),
                  range(900,400,-50),stringtoarr('New York, New York, USA',NUMCHARS))
    print(f.cmptypes)
    windunits = numpy.empty(1,winddtype_units)
    stationobs_units = numpy.empty(1,statdtype_units)
    windunits['speed'] = stringtoarr('m/s',NUMCHARS)
    windunits['direction'] = stringtoarr('degrees',NUMCHARS)
    stationobs_units['latitude'] = stringtoarr('degrees north',NUMCHARS)
    stationobs_units['longitude'] = stringtoarr('degrees west',NUMCHARS)
    stationobs_units['surface_wind'] = windunits
    stationobs_units['location_name'] = stringtoarr('None', NUMCHARS)
    stationobs_units['temp_sounding'] = stringtoarr('Kelvin',NUMCHARS)
    stationobs_units['press_sounding'] = stringtoarr('hPa',NUMCHARS)
    statdat.units = stationobs_units
# close and reopen the file.
    f.close()
    f = Dataset('compound_example.nc')
    print(f)
    statdat = f.variables['station_obs']
    print(statdat)
# print out data in variable.
    print('data in a variable of compound type:')
    print('----')
    for data in statdat[:]:
        for name in statdat.dtype.names:
            if data[name].dtype.kind == 'S': # a string
                # convert array of characters back to a string for display.
                units = chartostring(statdat.units[name])
                print(name,': value =',chartostring(data[name]),\
                          ': units=',units)
            elif data[name].dtype.kind == 'V': # a nested compound type
                units_list = [chartostring(s) for s in tuple(statdat.units[name])]
                print(name,data[name].dtype.names,': value=',data[name],': units=',\
                          units_list)
            else: # a numeric type.
                units = chartostring(statdat.units[name])
                print(name,': value=',data[name],': units=',units)
                print('----')
    f.close()
    f = Dataset('tst_vlen.nc','w')
    vlen_t = f.createVLType(numpy.int32, 'phony_vlen')
    x = f.createDimension('x',3)
    y = f.createDimension('y',4)
    vlvar = f.createVariable('phony_vlen_var', vlen_t, ('y','x'))
    import random
    data = numpy.empty(len(y)*len(x),object)
    for n in range(len(y)*len(x)):
        data[n] = numpy.arange(random.randint(1,10),dtype='int32')+1
        data = numpy.reshape(data,(len(y),len(x)))
        vlvar[:] = data
        print(vlvar)
        print('vlen variable =\n',vlvar[:])
        print(f)
        print(f.variables['phony_vlen_var'])
        print(f.vltypes['phony_vlen'])
        z = f.createDimension('z', 10)
        strvar = f.createVariable('strvar',str,'z')
        chars = '1234567890aabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    data = numpy.empty(10,object)
    for n in range(10):
        stringlen = random.randint(2,12)
        data[n] = ''.join([random.choice(chars) for i in range(stringlen)])
        strvar[:] = data
        print('variable-length string variable:\n',strvar[:])
        print(f)
        print(f.variables['strvar'])
    f.close()

if __name__ == "__main__":
    #init_from_file('FORCING.nc')
    #init_forcing_nc()
    fnc = CrocusForcing()
    fnc.close()
