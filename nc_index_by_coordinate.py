#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import pi, cos, sin, ravel, unravel_index

try:
    from scipy.spatial import cKDTree
except ImportError:
    print 'The kdtree_fast method requires the scipy.spatial module.'
    print 'Ignore this warning when using the tunnel_fast method.'
    
__author__ = 'kmu'

'''
The tunnel_fast and kdtree_fast methods are taken from the Unidata Python Workshop.
See (https://github.com/kmunve/unidata-python-workshop/blob/master/netcdf-by-coordinates.ipynb) for more information.
'''


def tunnel_fast(latvar,lonvar,lat0,lon0):
    '''
    Find closest point in a set of (lat,lon) points to specified point
    latvar - 2D latitude variable from an open netCDF dataset
    lonvar - 2D longitude variable from an open netCDF dataset
    lat0, lon0 - query point
    Returns iy,ix such that the square of the tunnel distance
    between (latval[iy,ix], lonval[iy,ix]) and (lat0, lon0)
    is minimum.

    :param latvar:
    :param lonvar:
    :param lat0:
    :param lon0:

    :return:

    '''
    rad_factor = pi/180.0 # for trignometry, need angles in radians
    # Read latitude and longitude from file into numpy arrays
    latvals = latvar[:] * rad_factor
    lonvals = lonvar[:] * rad_factor
    ny,nx = latvals.shape
    lat0_rad = lat0 * rad_factor
    lon0_rad = lon0 * rad_factor
    # Compute numpy arrays for all values, no loops
    clat,clon = cos(latvals),cos(lonvals)
    slat,slon = sin(latvals),sin(lonvals)
    delX = cos(lat0_rad)*cos(lon0_rad) - clat*clon
    delY = cos(lat0_rad)*sin(lon0_rad) - clat*slon
    delZ = sin(lat0_rad) - slat;
    dist_sq = delX**2 + delY**2 + delZ**2
    minindex_1d = dist_sq.argmin()  # 1D index of minimum element
    iy_min,ix_min = unravel_index(minindex_1d, latvals.shape)
    return iy_min,ix_min


def kdtree_fast(latvar,lonvar,lat0,lon0):
    '''
    :param latvar:
    :param lonvar:
    :param lat0:
    :param lon0:
    :return:
    '''
    rad_factor = pi/180.0 # for trignometry, need angles in radians
    # Read latitude and longitude from file into numpy arrays
    latvals = latvar[:] * rad_factor
    lonvals = lonvar[:] * rad_factor
    ny,nx = latvals.shape
    clat,clon = cos(latvals),cos(lonvals)
    slat,slon = sin(latvals),sin(lonvals)
    # Build kd-tree from big arrays of 3D coordinates
    triples = list(zip(ravel(clat*clon), ravel(clat*slon), ravel(slat)))
    kdt = cKDTree(triples)
    lat0_rad = lat0 * rad_factor
    lon0_rad = lon0 * rad_factor
    clat0,clon0 = cos(lat0_rad),cos(lon0_rad)
    slat0,slon0 = sin(lat0_rad),sin(lon0_rad)
    dist_sq_min, minindex_1d = kdt.query([clat0*clon0, clat0*slon0, slat0])
    iy_min, ix_min = unravel_index(minindex_1d, latvals.shape)
    return iy_min,ix_min

if __name__ == "__main__":
    print "..."