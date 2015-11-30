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
    """
    Currently I need to change this part in wsklima_parser.py

        def parse_get_stations_properties(xml_data):
        #TODO: need to fix the case when a file name is directly passed.


        if os.path.isfile(xml_data):
            root = etree.parse(xml_data)
        elif isinstance(xml_data, str):
            root = etree.fromstring(xml_data)



    :return:
    """
    sd = parse_get_stations_properties(r'./Test/Data/getStationsProperties.out.all.xml')
    db = CrocusStationDB('./Test/Data/all_eklima_stations.db')
    # db.create_station_db()
    for st in iter(sd.values()): # sd.itervalues() in Python 2.7
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
    # db.create_station_db()
    for s in iter(sd.values()):
        print(s)
        db.insert_station(s)
    db.close()


if __name__ == "__main__":
    # hourly_rr_ta_uu_ff_dd_po()
    # eklima_station_list()
    crocus_station_list()

