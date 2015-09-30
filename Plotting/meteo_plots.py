#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
from numpy import arange
"""
__author__: 'kmunve'

"""


def _temperature_plot(values, xticks=None, p_title=None, p_xlabel='Time', p_ylabel='Temperature'):
    """

    TODO: add a check if the values are in Kelvin, Fahrenheit, or Celsius and adjust plot parameters accordingly.
    TODO: rotate xlabels and change format to YYYY-MM-DD:HH
    :param values:
    :param xlabels:
    :return:
    """

    y = values
    if xticks is None:
        x = arange(len(y))
    else:
        x = xticks

    # Create figure
    plt.figure(figsize=(14,6))
    ax = plt.axes()

    # Set y limits
    ax.set_ylim(-10, 25)

    plt.plot(x, y, color='green', linewidth=2)
    plt.axhline(0.0, color='grey', linestyle='--')
    plt.title = p_title
    plt.xlabel = p_xlabel
    plt.ylabel = p_ylabel

def temperature_plot(values, xticks=None, p_title=None, p_xlabel='Time', p_ylabel='Temperature'):
    """
    Plot temperature values with envoked plt.show() for external use.
    """
    _temperature_plot(values, xticks, p_title, p_xlabel, p_ylabel)
    plt.show()
