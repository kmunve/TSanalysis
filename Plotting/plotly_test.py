#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import numpy as np
import plotly
import plotly.graph_objs as go
from wsklima_parser import parse_get_data

'''


Test gauge charts: https://plot.ly/python/gauge-charts/
for plotting avalanche problems in details

__author__ = 'kmu'
'''


def isMetDay(dt):
    if dt.hour == 6:
        return True
    else:
        return False

def removeNull(rr):
    if rr == -99999.0:
        return False
    else:
        return True


sd = parse_get_data('../Test/Data/eklima_data.xml')

station_id = '15890'

dates = sd[station_id]['index']
temperature = sd[station_id]['TA']['val']
precip = sd[station_id]['RR_1']['val']
#precip_24 = sd[station_id]['RR_24']['val']

precip_24 = list(filter(removeNull, sd[station_id]['RR_24']['val']))
dates_24 = list(filter(isMetDay, dates))

'''
dates = [datetime.datetime.today() - datetime.timedelta(days=i) for i in range(4)]

temperature = np.array([4, 1, -3, -17])
precip = [0, 3, 12, 15]
'''

ta_plot = go.Scatter(x=dates, y=temperature, name="Lufttemperatur (time)")
rr_plot = go.Bar(x=dates, y=precip, name="Nedbør (time)", yaxis="y2")
rr24_plot = go.Scatter(x=dates_24, y=precip_24, name="Nedbør (06-06)", yaxis="y2",
                       marker={'size': 15, 'symbol': 'square-cross-open'},
                       line={'shape': 'vh'}, fill='tozeroy')

data = [ta_plot, rr_plot, rr24_plot]
layout = go.Layout(
    title=station_id,
    xaxis={'type': 'date'},
    yaxis={'title': 'Celsius',
           'range': [-30, 20],
           'overlaying': 'y2',
           },
    yaxis2=dict(
        title='mm',
        # titlefont=dict(
        #     color='rgb(148, 103, 189)'
        # ),
        # tickfont=dict(
        #     color='rgb(148, 103, 189)'
        # ),
        range=[0, 50],
        side='right'
    )
)

fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename="ta-rr-plot.html")

"""
Vindrose

import plotly.plotly as py
import plotly.graph_objs as go

trace1 = go.Area(
    r=[77.5, 72.5, 70.0, 45.0, 22.5, 42.5, 40.0, 62.5],
    t=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'],
    name='11-14 m/s',
    marker=dict(
        color='rgb(106,81,163)'
    )
)
trace2 = go.Area(
    r=[57.49999999999999, 50.0, 45.0, 35.0, 20.0, 22.5, 37.5, 55.00000000000001],
    t=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'],
    name='8-11 m/s',
    marker=dict(
        color='rgb(158,154,200)'
    )
)
trace3 = go.Area(
    r=[40.0, 30.0, 30.0, 35.0, 7.5, 7.5, 32.5, 40.0],
    t=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'],
    name='5-8 m/s',
    marker=dict(
        color='rgb(203,201,226)'
    )
)
trace4 = go.Area(
    r=[20.0, 7.5, 15.0, 22.5, 2.5, 2.5, 12.5, 22.5],
    t=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'],
    name='< 5 m/s',
    marker=dict(
        color='rgb(242,240,247)'
    )
)
data = [trace1, trace2, trace3, trace4]
layout = go.Layout(
    title='Wind Speed Distribution in Laurel, NE',
    font=dict(
        size=16
    ),
    legend=dict(
        font=dict(
            size=16
        )
    ),
    radialaxis=dict(
        ticksuffix='%'
    ),
    orientation=270
)
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='polar-area-chart')


"""
