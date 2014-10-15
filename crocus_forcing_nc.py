#!/usr/bin/python
"""
Create a forcing netcdf file for the snow pack model Crocus.
"""
import datetime as dt
from netCDF4 import Dataset


def init_from_file(filename):
    # create a file (Dataset object, also the root group).
    f = Dataset(filename, 'r')
    print f.file_format
    print f.dimensions['Number_of_points']
    print f.dimensions['time']
    print f.variables.keys()
    for var in f.ncattrs():
        print var, getattr(f, var)
    print f.variables['Wind']
    print f.variables['Wind'].units
    f.variables['Wind'][:] = []
    print f.variables['Wind']
    f.close()



def init_forcing_nc(no_points=1):
    """
    Input no_points: Number of points used in the model grid
    """
    # create a file (Dataset object, also the root group).
    rootgrp = Dataset('FORCING.nc', 'w', format='NETCDF3_CLASSIC')
    print(rootgrp.file_format)

# dimensions.
    time = rootgrp.createDimension('time', None)
    number_of_points = rootgrp.createDimension('Number_of_points', no_points)
#lat = rootgrp.createDimension('lat', 73)
#lon = rootgrp.createDimension('lon', 144)
    print rootgrp.dimensions
    
    print time.isunlimited()
    print number_of_points.isunlimited()
    
# variables.
    # Scalars:
    
    FORC_TIME_STEP = rootgrp.createVariable('FORC_TIME_STEP','f8')
    FORC_TIME_STEP.units = 's'
    FORC_TIME_STEP.long_name = 'Forcing_Time_Step'


    # 1D
        
    time = rootgrp.createVariable('time','f8',('time',))
    # depends on FORC_TIME_STP units
    time.units = 'hours/seconds since '
    time.long_name = 'time'

    LAT = rootgrp.createVariable('LAT','f8',('Number_of_points',))
    LAT.units = 'degrees_north'
    LAT.long_name = 'latitude'

    LON = rootgrp.createVariable('LON','f8',('Number_of_points',))
    LON.units = 'degrees_east'
    LON.long_name = 'longitude'

    aspect = rootgrp.createVariable('aspect', 'f8', ('Number_of_points'))
    aspect.units = 'degrees from north'
    aspect.long_name = 'slope aspect'
    
    slope = rootgrp.createVariable('slope','f8',('Number_of_points',))
    slope.units = 'degrees from horizontal'
    slope.long_name = 'slope angle'

    UREF = rootgrp.createVariable('UREF','f8',('Number_of_points',))
    UREF.units = 'm'
    UREF.long_name = 'Reference_Height_for_Wind'
    
    ZREF = rootgrp.createVariable('ZREF','f8',('Number_of_points',))
    ZREF.units = 'm'
    ZREF.long_name = 'Reference_Height'
    
    ZS = rootgrp.createVariable('ZS','f8',('Number_of_points',))
    ZS.units = 'm'
    ZS.long_name = 'altitude'
    

    # 2D

    CO2air = rootgrp.createVariable('CO2air','f8',('time', 'Number_of_points',))
    CO2air.units = 'kg/m3'
    CO2air.long_name = 'Near_Surface_CO2_Concentration'
    
    DIR_SWdown = rootgrp.createVariable('DIR_SWdown','f8',('Number_of_points',))
    DIR_SWdown.units = 'W/m2'
    DIR_SWdown.long_name = 'Surface_Indicent_Direct_Shortwave_Radiation'
    
    HUMREL = rootgrp.createVariable('HUMREL','f8',('time', 'Number_of_points',))
    HUMREL.units = '%'
    HUMREL.long_name = 'Relative Humidity'

    LWdown = rootgrp.createVariable('LWdown','f8',('time', 'Number_of_points',))
    LWdown.units = 'W/m2'
    LWdown.long_name = 'Surface_Incident_Longwave_Radiation'
    
    NEB = rootgrp.createVariable('NEB','f8',('time', 'Number_of_points',))
    NEB.units = 'between 0 and 1'
    NEB.long_name = 'Nebulosity'
    
    PSurf = rootgrp.createVariable('PSurf','f8',('time', 'Number_of_points',))
    PSurf.units = 'Pa'
    PSurf.long_name = 'Surface_Pressure'
    
    Qair = rootgrp.createVariable('Qair','f8',('time', 'Number_of_points',))
    Qair.units = 'Kg/Kg'
    Qair.long_name = 'Near_Surface_Specific_Humidity'
    
    Rainf = rootgrp.createVariable('Rainf','f8',('time', 'Number_of_points',))
    Rainf.units = 'kg/m2/s'
    Rainf.long_name = 'Rainfall_Rate'

    SCA_SWdown = rootgrp.createVariable('SCA_SWdown','f8',('time', 'Number_of_points',))
    SCA_SWdown.units = 'W/m2'
    SCA_SWdown.long_name = 'Surface_Incident_Diffuse_Shortwave_Radiation'
    
    Snowf = rootgrp.createVariable('Snowf','f8',('time', 'Number_of_points',))
    Snowf.units = 'kg/m2/s'
    Snowf.long_name = 'Snowfall_Rate'

    Tair = rootgrp.createVariable('Tair','f8',('time', 'Number_of_points',))
    Tair.units = 'K'
    Tair.long_name = 'Near_Surface_Air_Temperature'
    
    Wind = rootgrp.createVariable('Wind','f8',('time', 'Number_of_points',))
    Wind.units = 'm/s'
    Wind.long_name = 'Wind_Speed'
    
    Wind_DIR = rootgrp.createVariable('Wind_DIR','f8',('time', 'Number_of_points',))
    Wind_DIR.units = 'deg'
    Wind_DIR.long_name = 'Wind_Direction'


#     = rootgrp.createVariable('','f8',('Number_of_points',))
#    .units = ''
#    .long_name = ''

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
    print nc.variables['time']

    for col in df.columns:
        if col in id_dict.keys():
            print df[col], nc.variables[id_dict[col]]
            nc.variables[id_dict[col]] = df[col]
            print nc.variables[id_dict[col]]

    nc.close()

def get_nc_time(df_index):
    
    # 
    print df_index[0]
    tinterval = df_index[1]-df_index[0]
    print tinterval
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
    init_forcing_nc()