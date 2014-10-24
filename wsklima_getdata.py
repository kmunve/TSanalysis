#!/usr/bin/python
"""
Author: kmunve
"""
import requests

class wsKlimaRequest():
    """
    Creates a request to eklima.met.no using the wsKlima methods.
    See: http://eklima.met.no/wsKlima/start/start_no.html

    Usage: see "test_..." functions at the end of this file.

    """    
    def __init__(self, method, params=None):
        
        self.wsmethod = method
        self.wsmethods = ['getElementsProperties', 'getElementsFromTimeserieType', 'getStationsFromTimeserieTypeElemCodes', 'getStationsFromTimeserieTypeStationsElemCode', 'getMetData']


        if self.wsmethod not in self.wsmethods:
            print "Please choose a valid method:\n"
            for _m in self.wsmethods:
                print _m

        self.params = params
        self.base_url= 'http://eklima.met.no/met/MetService'
        self.wsklima_url = self.base_url

        self._create_wsklima_url()
        

    def _create_wsklima_url(self):

        if self.wsmethod == 'getMetData':
            self.wsklima_url = "{0}?invoke=getMetData&timeserietypeID={1}&format={2}&from={3}&to={4}&stations={5}&elements={6}&hours={7}&months={8}&username={9}".format(self.base_url, self.params['timeserietypeID'], self.params['format'], self.params['from'], self.params['to'], ",".join(map(str, self.params['stations'])), ",".join(map(str, self.params['elements'])), ",".join(map(str, self.params['hours'])), self.params['months'], self.params['username'])
            
        
        elif self.wsmethod == 'getStationsFromTimeserieTypeElemCodes':
            # params = timeserietypeID, elem_codes, username
            self.wsklima_url = "{0}?invoke=getStationsFromTimeserieTypeElemCodes&timeserietypeID={1}&elem_codes={2}&username={3}".format(self.base_url, self.params['timeserietypeID'], ",".join(map(str, self.params['elem_codes'])), self.params['username'])

        elif self.wsmethod == 'getStationsFromTimeserieTypeStationsElemCode':
            # params = timeserietypeID, elem_codes, username, stations
            self.wsklima_url = "{0}?invoke=getStationsFromTimeserieTypeStationsElemCode&timeserietypeID={1}&stations={4}&elem_codes={2}&username={3}".format(self.base_url, self.params['timeserietypeID'], ",".join(map(str, self.params['elem_codes'])), self.params['username'], ",".join(map(str, self.params['stations'])))
            
        elif self.wsmethod == 'getElementsFromTimeserieType':
            # params = timeserietypeID
            self.wsklima_url = "{0}?invoke=getElementsFromTimeserieType&timeserietypeID={1}".format(self.base_url, self.params['timeserietypeID'])
            
        elif self.wsmethod == 'getElementsProperties':
            # params = language, elem_codes
            self.wsklima_url = "{0}?invoke=getElementsProperties&language={1}&elem_codes={2}".format(self.base_url, self.params['language'], ",".join(map(str, self.params['elem_codes'])))


        else:
            print "Could not create url!"



    def get(self):
        ### Returns a requests.Response object                                                                      
        return requests.get(self.wsklima_url)


    def _output_example(self):
        if self.wsmethod == 'getStationsFromTimeserieTypeElemCodes':
            print """Example response from 'getStationsFromTimeserieTypeElemCodes':\n\n
            <?xml version='1.0' encoding='UTF-8'?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<SOAP-ENV:Body>
<ns1:getStationsFromTimeserieTypeElemCodesResponse xmlns:ns1="http://no/met/metdata/MetService.wsdl" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<return xmlns:ns2="http://schemas.xmlsoap.org/soap/encoding/" xsi:type="ns2:Array" xmlns:ns3="http://no.met.metdata/IMetService.xsd" ns2:arrayType="ns3:no_met_metdata_StationProperties[1964]">
<item xsi:type="ns3:no_met_metdata_StationProperties">
<amsl xsi:type="xsd:int">564</amsl>
<department xsi:type="xsd:string">HEDMARK</department>
<fromDay xsi:type="xsd:int">1</fromDay>
<fromMonth xsi:type="xsd:int">7</fromMonth>
<fromYear xsi:type="xsd:int">1968</fromYear>
<latDec xsi:type="xsd:double">61.5581</latDec>
<latLonFmt xsi:type="xsd:string">decimal_degrees</latLonFmt>
<lonDec xsi:type="xsd:double">12.499</lonDec>
<municipalityNo xsi:type="xsd:int">428</municipalityNo>
<name xsi:type="xsd:string">LINNES</name>
<stnr xsi:type="xsd:int">60</stnr>
<toDay xsi:type="xsd:int">0</toDay>
<toMonth xsi:type="xsd:int">0</toMonth>
<toYear xsi:type="xsd:int">0</toYear>
<utm_e xsi:type="xsd:int">367134</utm_e>
<utm_n xsi:type="xsd:int">6827504</utm_n>
<utm_zone xsi:type="xsd:int">33</utm_zone>
<wmoNo xsi:type="xsd:int">0</wmoNo>
</item>
\n
            """

        else:
            print "No valid method given!"
    
def test_getStationsFromTimeserieTypeElemCodes():
    wr = wsKlimaRequest('getStationsFromTimeserieTypeElemCodes', {'timeserietypeID': 2, 'elem_codes': ['RR_1', 'RR_24', 'TA', 'UU', 'FF'], 'username': ""}).get()
    print wr.text
    print wr.url


def test_getStationsFromTimeserieTypeStationsElemCode():
    wr = wsKlimaRequest('getStationsFromTimeserieTypeStationsElemCode', {'timeserietypeID': 2, 'stations': [],  'elem_codes': ['RR_1', 'RR_24', 'TA', 'UU', 'FF'], 'username': ""})
    rsp = wr.get()              # get the requests.Response
    print rsp.text
    print rsp.url
            
    
def test_getMetData():
    wr = wsKlimaRequest('getMetData', {'timeserietypeID': 2, 'format': "", 'from': '2014-01-01', 'to': '2014-01-31', 'stations': [52860,], 'elements': ['TA', 'RR_1' , 'RR_24', 'FF', 'UU'], 'hours': range(0,24), 'months': "", 'username': ""}).get()
    print wr.text
    print wr.url


def test_getElementsFromTimeserieType():
    wr = wsKlimaRequest('getElementsFromTimeserieType', {'timeserietypeID': 2}).get()
    print wr.text
    print wr.url

 


if __name__ == "__main__":
#    test_getStationsFromTimeserieTypeElemCodes()
#    test_getElementsFromTimeserieType()
    test_getMetData()
        
