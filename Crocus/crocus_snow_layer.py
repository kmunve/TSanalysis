#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

'''


__author__ = 'kmu'

- *XWSNOW* : uniform value to initialize snow content, one for each layer
- *XZSNOW* : depth of snow layers (m). Alternative to *XWSNOW*.
- *XTSNOW* : uniform value to initialize snow temperature, one for each layer
- *XLWCSNOW* : snow liquid water content (kg/m3)
- *XRSNOW* : uniform value to initialize snow density, one for each layer
- *XASNOW* : uniform value to initialize snow albedo
- *XSG1SNOW* : uniform value to initialize snow layers grain feature 1 for Crocus, one for each layer
- *XSG2SNOW* : uniform value to initialize snow layers grain feature 2 for Crocus, one for each layer
- *XHISTSNOW* : uniform value to initialize snow layer grain historical parameter for Crocus, one for each layer
- *XAGESNOW* : uniform value to initialize snow grain age for Crocus, one for each layer
- *LSWEMAX* : logical switch to set an upper limit on initial snow water equivalent
- *XSWEMAX* : upper limit of initial snow water equivalent

'''


def crocus_snow_layer(z, ts, lwc, rho, age, sg1, sg2, hist):
    pass


def write_namelist(snow_layers):
    insert_str = ""
    xz = []
    for layer in snow_layers:
        xz.append(layer['z'])
        xts.append(layer['ts'])



        "XZSNOW = {0.2d},".format(z)

