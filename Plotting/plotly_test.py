#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import plotly
import datetime
import itertools
print(plotly.__version__)  # version >1.9.4 required
from plotly.graph_objs import Scatter, Layout, Bar

'''


Test gauge charts: https://plot.ly/python/gauge-charts/
for plotting avalanche problems in details

__author__ = 'kmu'
'''

dates = [datetime.datetime.today() - datetime.timedelta(days=i) for i in range(4)]
#dates = [1, 2, 3, 4]

temperature = [4, 1, -3, -7]
precip = [0, 3, 12, 15]

plotly.offline.plot({
    "data": [
        Scatter(x=dates, y=temperature),
        Bar(x=dates, y=precip)
    ],
    "layout": Layout(
        title="Temperature"
    )
})
