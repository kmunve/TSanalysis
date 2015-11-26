#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime as dt
import numpy as np
from lxml import etree

"""
__author__: kmunve

"""


def parse_get_data(xml_data):
    """
    Converts the XML return from a wsklima.getData() call to a Python dictionary.
    For more info on wsklima see eklima.met.no.

    Structure of the returned Python dictionary
    A dictionary with a key for each station:
        station_dict['<station-id>']
            ...containing a dictionary with the following keys:
            ['index']: list of datetime object of the observation time
            ['<weather-element>']: dictionary with the following keys:
                ['val']: list of values at observation time
                ['q']: list of quality flags corresponding to 'val'

    Usage:

    Get XML file from eklima.met.no, e.g. by using wsklima_requests.py or
    http://eklima.met.no/met/MetService?operation=getMetData

    Hand the XML file/string to parse_get_data(xml_data), e.g.

        sd = parse_get_data('54110.xml')

    :param xml_data: string or file containing XML data
    :return: station_dict
    """
    station_dict = {} # station dictionary

    tree = etree.parse(open(xml_data))

    root = tree.getroot()

    # Get all item-tags that are a child of the timeStamp-tag
    TSitems = root.xpath('//timeStamp/item')

    # loop over all timestamps
    for TS in TSitems:
        # extract datetime
        tstamp = TS.xpath('from')[0].text
        # Convert string to datetime
        _index = dt.datetime.strptime(tstamp, '%Y-%m-%dT%H:%M:%S.000Z')

        # Get all item-tags that are a child of the current location-tag
        LOCitmes = TS.xpath('location/item')
        for LOC in LOCitmes:
            # Retrieve station id
            stat_id = LOC.xpath('id')[0].text

            # Init new station dict if necessary
            if stat_id not in station_dict.keys():
                station_dict[stat_id] = {}
                station_dict[stat_id]['index'] = []

            # Append the time stamp
            station_dict[stat_id]['index'].append(_index)

            # Get all item-tags that are a child of the weatherElement-tag
            WEitems = LOC.xpath('weatherElement/item')
            # Loop over the weather elements
            for WE in WEitems:
                we_id = WE.xpath('id')[0].text # Retrieve parameter name
                we_q = np.int(WE.xpath('quality')[0].text) # Retrieve quality flag
                we_val = np.float(WE.xpath('value')[0].text) # Retrieve measured value

                # Add a new dictionary if the weather element does not exist, yet.
                if we_id not in station_dict[stat_id].keys():
                    station_dict[stat_id][we_id] = {}
                    station_dict[stat_id][we_id]['val'] = []
                    station_dict[stat_id][we_id]['q'] = []

                # Append value and quality for the current time step
                station_dict[stat_id][we_id]['val'].append(we_val)
                station_dict[stat_id][we_id]['q'].append(we_q)

    return station_dict


def parse_get_stations_properties(xml_data):

    if type(xml_data) == 'string':
        root = etree.fromstring(xml_data)
    elif type(xml_data) == 'file':
        root = etree.parse(open(xml_data))
    else:
        print("Please provide a string or file object. Got {0}".format(type(xml_data)))

    stations = root.xpath('//return/item')

    """
    Available properties:
    amsl
    department
    fromDay
    fromMonth
    fromYear
    latDec
    latLonFmt
    lonDec
    municipalityNo
    name
    stnr
    toDay
    toMonth
    toYear
    utm_e
    utm_n
    utm_zone
    wmoNo
    """
    stations_dict = {}

    for station in stations:
        amsl = station.xpath('amsl')[0].text
        department = station.xpath('department')[0].text
        fromDay = station.xpath('fromDay')[0].text
        fromMonth = station.xpath('fromMonth')[0].text
        fromYear = station.xpath('fromYear')[0].text
        latDec = station.xpath('latDec')[0].text
        latLonFmt = station.xpath('latLonFmt')[0].text
        lonDec = station.xpath('lonDec')[0].text
        municipalityNo = station.xpath('municipalityNo')[0].text
        name = station.xpath('name')[0].text
        stnr = station.xpath('stnr')[0].text
        toDay = station.xpath('toDay')[0].text
        toMonth = station.xpath('toMonth')[0].text
        toYear = station.xpath('toYear')[0].text
        utm_e = station.xpath('utm_e')[0].text
        utm_n = station.xpath('utm_n')[0].text
        utm_zone = station.xpath('utm_zone')[0].text
        wmoNo = station.xpath('wmoNo')[0].text

        insert_stations_dict(stations_dict,
                        amsl,
                        department,
                        fromDay,
                        fromMonth,
                        fromYear,
                        latDec,
                        latLonFmt,
                        lonDec,
                        municipalityNo,
                        name,
                        stnr,
                        toDay,
                        toMonth,
                        toYear,
                        utm_e,
                        utm_n,
                        utm_zone,
                        wmoNo)

    return stations_dict

if __name__ == '__main__':
    import pylab
    sd = parse_get_data('54110.xml')
    print(sd['54110'])
    print(sd['12290'])
    pylab.plot(sd['12290']['index'], sd['12290']['TA']['val'])
    pylab.show()
