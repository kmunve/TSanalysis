#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: kmunve

Todo:
- make diff methods for different station list: all_input, all_but_rad, ta_uu_ff, rr_ta, ...
- make list over radiation stations
- export station list to Google kmz-file

TODO: move to folder util/eklima
"""
from __future__ import print_function
from wsklima_requests import wsKlimaRequest
import json
from lxml import etree
from crocus_station_db import CrocusStationDB
from wsklima_parser import parse_get_stations_properties

def hourly_rr_ta_uu_ff_dd_po():
    
    wr = wsKlimaRequest('getStationsFromTimeserieTypeStationsElemCode', {'stations': [], 'timeserietypeID': 2, 'elem_codes': ['RR_1', 'RR_24', 'TA', 'UU', 'FF', 'DD', 'PO'], 'username': ""})
    rsp = wr.get()

    # Parse XML string
    root = etree.fromstring(rsp.content)

    # Temporary list of element codes
    station_list = []

    # prepare outfile
    outfile = 'stations_hourly_rr_ta_uu_ff_dd_po.txt'
    fid = open(outfile, 'w')
    fid.write('#\tSNR\tSTNR\tLAT_DEC\tLON_DEC\tAMSL\tST_NAME\tDepartment\n')
    # Iterate over all "item" elements
    for element in root.iter("item"):
        # Add only stations that still are operative
        if int(element.find('toYear').text) == 0:
            station_list.append(int(element.find('stnr').text))
            fid.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n".format(element.find('wmoNo').text.encode('utf-8'), element.find('stnr').text, element.find('latDec').text, element.find('lonDec').text, element.find('amsl').text, element.find('name').text.encode('utf-8'), element.find('department').text.encode('utf-8')))
            
    print("Found {0} stations.\nWritten to {1}".format(len(station_list), outfile))

    fid.close()


def eklima_station_list():
    sd = parse_get_stations_properties(r'./Test/Data/getStationsProperties.out.all.xml')
    db = CrocusStationDB('./Test/Data/all_eklima_stations.db')
    db.create_station_db()
    for st in sd.itervalues():
        print(st)
        db.insert_station(st)
    db.close()


def crocus_station_list():
    stat = json.load(open('Test/Data/crocus_stations.json', 'r'))
    station_list = stat['crocus_stations']

    wr = wsKlimaRequest('getStationsProperties', {'stations': station_list, 'username': ''})
    rsp = wr.get()
    print(type(rsp.content))
    sd = parse_get_stations_properties(rsp.content)

    # sd = crocus_station_list()
    print(sd['13655'])
    db = CrocusStationDB('./Test/Data/stations.db')
    #db.create_station_db()
    for s in iter(sd.values()):
        print(s)
        db.insert_station(s)
    db.close()

    '''
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


def insert_stations_dict(stations_dict,
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
    '''
if __name__ == "__main__":
    # hourly_rr_ta_uu_ff_dd_po()
    # eklima_station_list()
    crocus_station_list()

