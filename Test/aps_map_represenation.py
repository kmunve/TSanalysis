#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
__author__ = kmu

'''

import numpy as np
import matplotlib.pylab as plt

aspect = np.zeros((10, 15), float)
elevation_band = np.zeros((10, 15), float)
avalanche_problem = np.zeros((10, 15), float)
danger_level = np.ones((10, 15), float)

aspect[3:5, 7:10] = 40.0
aspect[6:9, 2:7] = 40.0

elevation_band[0:5, 0:10] = 800.0
elevation_band[5:11, 0:10] = 1200.0
elevation_band[0:11, 10:16] = 500.0

avalanche_problem[2:9, 2:13] = 1.0

asp_mask = np.ma.masked_where(aspect == 40.0, aspect)
ele_mask = np.ma.masked_where(elevation_band == 1200.0, elevation_band)

res = asp_mask.mask * ele_mask.mask

print(asp_mask, ele_mask)
print(avalanche_problem * res)


plt.imshow(avalanche_problem * res)
plt.colorbar()
plt.show()
