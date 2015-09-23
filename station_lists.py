#!/usr/bin/env python
"""
Author. kmunve


Todo:
- make diff methods for different station list: all_input, all_but_rad, ta_uu_ff, rr_ta, ...
- make list over radiation stations
- export station list to Google kmz-file
"""
from lxml import etree
from wsklima_requests import wsKlimaRequest


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
            
    print "Found {0} stations.\nWritten to {1}".format(len(station_list), outfile)

    fid.close()


if __name__ == "__main__":
    hourly_rr_ta_uu_ff_dd_po()
