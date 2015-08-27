#!/usr/bin/env python

import json
import datetime
import pandas as pd
import numpy as np
import pylab as mpl
doc = json.load(open('125.json'))

header = doc['obs_description']

data = {'obs_time': [],
'air_temperature': [],
'snow_height': [],
'snow_fall_height': [],
'humidity': [],
'wind_speed': [],
'wind_speed_max': [],
'wind_direction': []
}
for i in doc['obs_data']:
    data['obs_time'].append(datetime.datetime.strptime(i['obs_period'], '%Y-%m-%d %H:%M:%S'))
    data['air_temperature'].append(np.float(i['tmp2']))
    data['snow_height'].append(np.float(i['sd']))
    data['snow_fall_height'].append(np.float(i['sdfsw']))
    data['humidity'].append(np.float(i['humid']))

    # Bad data is either null or 999.9.
    # Replace those values by np.nan.
    try:
        _wspd = np.float(i['wspd'])
        if _wspd > 250.0:
            _wspd = np.nan
        data['wind_speed'].append(_wspd)
    except ValueError:
        data['wind_speed'].append(np.nan)

    try:
        _wspd_max = np.float(i['wspd_max'])
        if _wspd_max > 250.0:
            _wspd_max = np.nan
        data['wind_speed_max'].append(_wspd_max)
    except ValueError:
        data['wind_speed_max'].append(np.nan)
    try:
        data['wind_direction'].append(np.float(i['wdir']))
    except ValueError:
        data['wind_direction'].append(np.nan)

df = pd.DataFrame(data)
# Now set the observation time as the index
df.set_index('obs_time', inplace=True)
print df.describe()

#df.plot(x='obs_time', y='air_temperature')
df.plot(subplots=True)


#mpl.title("Station: {0}\nLat: {1}, Lon: {2}, Elevation: {3}masl".format(header['station_id'],
#header['lat'], header['lon'], header['alt']))

#mpl.gcf().savefig(header['station_id']+'.png', dpi=90)
mpl.show()
