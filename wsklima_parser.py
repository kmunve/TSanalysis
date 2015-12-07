#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import datetime as dt
import numpy as np
from lxml import etree
from io import StringIO, BytesIO

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
    #TODO: need to fix the case when a file name is directly passed.


    # if os.path.isfile(xml_data):
    #     root = etree.parse(xml_data)
    if isinstance(xml_data, str):
        root = etree.fromstring(xml_data)
    elif isinstance(xml_data, bytes):
        root = etree.parse(BytesIO(xml_data))
    else:
        print("Please provide a string, file or file object. Got {0}".format(type(xml_data)))

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

        _insert_stations_dict(stations_dict,
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


def _insert_stations_dict(stations_dict,
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
                        wmoNo):

    stations_dict[stnr] = {}
    stations_dict[stnr]['amsl'] = int(amsl)
    stations_dict[stnr]['department'] = department
    stations_dict[stnr]['fromDay'] = int(fromDay)
    stations_dict[stnr]['fromMonth'] = int(fromMonth)
    stations_dict[stnr]['fromYear'] = int(fromYear)
    stations_dict[stnr]['latDec'] = float(latDec)
    stations_dict[stnr]['latLonFmt'] = latLonFmt
    stations_dict[stnr]['lonDec'] = float(lonDec)
    stations_dict[stnr]['municipalityNo'] = int(municipalityNo)
    stations_dict[stnr]['name'] = name
    stations_dict[stnr]['stnr'] = int(stnr)
    stations_dict[stnr]['toDay'] = int(toDay)
    stations_dict[stnr]['toMonth'] = int(toMonth)
    stations_dict[stnr]['toYear'] = int(toYear)
    stations_dict[stnr]['utm_e'] = int(utm_e)
    stations_dict[stnr]['utm_n'] = int(utm_n)
    stations_dict[stnr]['utm_zone'] = int(utm_zone)
    stations_dict[stnr]['wmoNo'] = int(wmoNo)


def parse_get_elements_from_timeserie_type_station(xml_data):
    #TODO: need to fix the case when a file name is directly passed.


    # if os.path.isfile(xml_data):
    #     root = etree.parse(xml_data)
    if isinstance(xml_data, str):
        root = etree.fromstring(xml_data)
    elif isinstance(xml_data, bytes):
        root = etree.parse(BytesIO(xml_data))
    else:
        print("Please provide a string, file or file object. Got {0}".format(type(xml_data)))

    elements = root.xpath('//return/item')

    """
    Available properties:
    - description
    - elemCode
    - elemGroup
    - elemNo
    - fromdate
    - todate
    - language
    - name
    - unit
    """

    elements_dict = {}

    for element in elements:
        description = element.xpath('description')[0].text
        elemCode = element.xpath('elemCode')[0].text
        elemGroup = element.xpath('elemGroup')[0].text
        elemNo = element.xpath('elemNo')[0].text
        fromdate = element.xpath('fromdate')[0].text
        todate = element.xpath('todate')[0].text
        language = element.xpath('language')[0].text
        name = element.xpath('name')[0].text
        unit = element.xpath('unit')[0].text

        _insert_elements_dict(elements_dict,
                        description,
                        elemCode,
                        elemGroup,
                        elemNo,
                        fromdate,
                        todate,
                        language,
                        name,
                        unit)

    return elements_dict


def _insert_elements_dict(elements_dict,
                        description,
                        elemCode,
                        elemGroup,
                        elemNo,
                        fromdate,
                        todate,
                        language,
                        name,
                        unit):

    time_format = "%Y-%m-%dT%H:%M:%S.000Z"

    elements_dict[elemCode] = {}
    elements_dict[elemCode]['description'] = description
    elements_dict[elemCode]['elemGroup'] = elemGroup
    elements_dict[elemCode]['elemNo'] = int(elemNo)
    try:
        elements_dict[elemCode]['fromdate'] = dt.datetime.strptime(fromdate, time_format)
    except TypeError:
        elements_dict[elemCode]['fromdate'] = None
    try:
        elements_dict[elemCode]['todate'] = dt.datetime.strptime(todate, time_format)
    except TypeError:
        elements_dict[elemCode]['todate'] = None
    elements_dict[elemCode]['language'] = language
    elements_dict[elemCode]['name'] = name
    elements_dict[elemCode]['unit'] = unit


if __name__ == '__main__':
    import pylab
    sd = parse_get_data('54110.xml')
    print(sd['54110'])
    print(sd['12290'])
    pylab.plot(sd['12290']['index'], sd['12290']['TA']['val'])
    pylab.show()
